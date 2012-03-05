#coding:utf8

from sqlalchemy.orm import sessionmaker
session_maker = None

def init():
    global session_maker
    from ljn.Model import init as model_init, BaseModel
    model_init()

    session_maker = sessionmaker(BaseModel)

def get_session():
    """ @rtype: Session """
    return session_maker()


class Repository(object):
    def __init__(self):
        from ArticleRepository import ArticleRepository

        articles = ArticleRepository()
