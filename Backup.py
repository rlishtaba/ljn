#coding:utf8
from os.path import join, exists
import g
import json
import logging

log = logging.getLogger(__name__)

"""

Redis scheme:
ljn:user_name:backups => list of 'id|date|md5|original size|compressed size|computer'
ljn:user_name:backup_id => next backup id
ljn:user_name:backup:id:content => backup data (bz2 compressed db file)


"""

CFG_FILE = join(g.DATA_DIR, 'backup.cfg')
DATA_FILE = join(g.DATA_DIR, 'ljn.db')

def ask_cfg(file_name):
    user_name = raw_input('User name:')
    host_name = raw_input('Host name:')
    redis_url = raw_input('Redis url:')
    with file(file_name, 'wt') as fp:
        data = {'user_name': user_name, 'redis_url': redis_url, 'host_name': host_name}
        fp.write(json.dumps(data, indent=4, sort_keys=True))

def read_cfg(file_name):
    if not exists(file_name):
        return None

    cfg = json.loads(file(file_name, 'rb').read())
    if 'user_name' in cfg and 'redis_url' in cfg and 'host_name' in cfg:
        return cfg

    return None


def get_data_file_md5():
    from hashlib import md5
    if not exists(DATA_FILE):
        return ''
    return md5(file(DATA_FILE, 'rb').read()).hexdigest()


def get_data_file():
    from bz2 import compress
    from hashlib import md5

    data = file(DATA_FILE, 'rb').read()
    digest = md5(data).hexdigest()
    cdata = compress(data)
    return cdata, digest, len(data), len(cdata)

def get_date_str():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def restore_data(content):
    if content is None:
        print 'failed to get content of the backup'
        return

    if exists(DATA_FILE):
        import shutil
        shutil.move(DATA_FILE, DATA_FILE + '.' + get_date_str())

    from bz2 import decompress
    data = decompress(content)

    with file(DATA_FILE, 'wb') as fp:
        fp.write(data)

def create_conn():
    cfg = read_cfg(CFG_FILE)
    if cfg is None:
        print 'invalid cfg file'
        return None

    from urlparse import urlparse
    up = urlparse(cfg['redis_url'])
    if up.scheme != 'redis':
        print 'url scheme should be redis!'
        return None

    import redis
    return redis.Redis(up.hostname, up.port, password=up.password)

def backup_data(r=None):
    if not exists(DATA_FILE):
        return None

    if r is None:
        r = create_conn()
        if r is None:
            log.error('connect to redis server error!')
            return None

    cfg = read_cfg(CFG_FILE)
    PREFIX = 'ljn:%s:' % cfg['user_name']

    cdata, md5, osize, csize = get_data_file()
    id = r.incr(PREFIX + 'backup_id')
    r.rpush(PREFIX + 'backups', '%s|%s|%s|%s|%s|%s' % (id, get_date_str(), md5, osize, csize, cfg['host_name']))
    r.set(PREFIX + 'backup:%s:content' % id, cdata)
    log.info('backup data to server done')
    return id

def update_data(r=None):
    """ @type r: Redis """
    if r is None:
        r = create_conn()
        if r is None:
            return None

    cfg = read_cfg(CFG_FILE)
    PREFIX = 'ljn:%s:' % cfg['user_name']
    info = r.lrange(PREFIX + 'backups', -1, -1)
    if not info:
        return

    id, date, md5, osize, csize, host = info[0].split('|', 5)
    if get_data_file_md5() == md5:
        log.info('data file is up to date')
        return

    restore_data(r.get(PREFIX + 'backup:%s:content' % id))
    log.info('restore data from server done')

def main():
    if not exists(CFG_FILE):
        ask_cfg(CFG_FILE)

    cfg = None
    while cfg is None:
        cfg = read_cfg(CFG_FILE)
        if cfg is None:
            ask_cfg(CFG_FILE)

    PREFIX = 'ljn:%s:' % cfg['user_name']

    r = create_conn()
    if r is None:
        return

    print 'usage:\n\tl\tlist backups on server,\n\tq\tquit,\n\tb\tbackup to server,\n\tr [id]\trestore backup'
    while True:
        cmd = raw_input('>>> ').strip().lower()
        if cmd == 'q':
            break
        elif cmd == 'l':
            backups = r.lrange(PREFIX + 'backups', 0, -1) or []
            print 'backups:'
            print 'id|date|md5|original size|compressed size|computer'.split('|')
            print '-' * 60
            for b in backups:
                print b.split('|', 5)
        elif cmd == 'b':
            id = backup_data(r)
            if id is None:
                print 'backup failed!'
            else:
                print 'backup done, id is', id
        elif cmd.startswith('r '):
            id = cmd.split(' ', 1)[1].strip()
            if not id.isdigit():
                print 'usage: r [backup id]'
                continue

            restore_data(r.get(PREFIX + 'backup:%s:content' % id))
        else:
            print 'unknown command "%s"' % cmd

if __name__ == '__main__':
    main()
