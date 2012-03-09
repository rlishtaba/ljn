#coding:utf8
from ljn.Model import Article, ArticleNewWord, Word

session_maker = None

def add_test_data():
    from ljn.Model import Category
    s = session_maker()
    if not len(Category.all(s)):
        s.add(Category(u'c1'))
        s.add(Category(u'c2'))

    if not len(Article.all(s)):
        s.add(Article('this is content 1', Category.find_by_name(s, u'c1'), u'title of a1'))
        s.add(Article('this is content 2', Category.find_by_name(s, u'c1'), u'title of a2'))
        s.add(Article('this is content 3', Category.find_by_name(s, u'c2'), u'title of a3'))

    article = Category.find_by_name(s, u'c1').articles[0]
    if not len(article.new_words):
        w = Word('is')
        article.new_words.append(ArticleNewWord(article, w, 'is'))

    s.commit()


def init():
    global session_maker
    from ljn.Model import init as model_init, BaseModel
    model_init()

    from sqlalchemy.orm import sessionmaker
    session_maker = sessionmaker(BaseModel.metadata.bind)

    add_test_data()

def get_session():
    """ @rtype: sqlalchemy.orm.session.Session """
    return session_maker()

