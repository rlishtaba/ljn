#coding:utf8

from sqlalchemy.orm import sessionmaker
session_maker = None

def init():
    global session_maker
    from ljn.Model import init as model_init, BaseModel, Category
    model_init()

    session_maker = sessionmaker(BaseModel.metadata.bind)
    s = session_maker()
    if not len(Category.all(s)):
        s.add(Category(u'c1'))
        s.add(Category(u'c2'))
        s.commit()

def get_session():
    """ @rtype: Session """
    return session_maker()


class Repository(object):
    def __init__(self):
        from ArticleRepository import ArticleRepository

        articles = ArticleRepository()
