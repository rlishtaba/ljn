#coding:utf8
from ljn.Model import Article

session_maker = None

def init():
    global session_maker
    from ljn.Model import init as model_init, BaseModel, Category
    model_init()

    from sqlalchemy.orm import sessionmaker
    session_maker = sessionmaker(BaseModel.metadata.bind)
    s = session_maker()
    if not len(Category.all(s)):
        s.add(Category(u'c1'))
        s.add(Category(u'c2'))

    if not len(Article.all(s)):
        s.add(Article('this is content 1', Category.find_by_name(s, u'c1'), u'title of a1'))
        s.add(Article('this is content 2', Category.find_by_name(s, u'c1'), u'title of a2'))
        s.add(Article('this is content 3', Category.find_by_name(s, u'c2'), u'title of a3'))

    s.commit()

def get_session():
    """ @rtype: Session """
    return session_maker()

