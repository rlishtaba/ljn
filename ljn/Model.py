#coding:utf8

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UnicodeText, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

BaseModel = declarative_base()

def init():
    from os.path import join
    from g import DATA_DIR
    from sqlalchemy import create_engine

    DB_FILE = join(DATA_DIR, 'ljn.db')
    BaseModel.metadata.create_all(create_engine('sqlite:///' + DB_FILE.replace('\\', '/')))


class Category(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    articles = relationship("Article", backref="category")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_by_name(session, name):
        """ @rtype: Category """
        return session.query(Category).filter(Category.name == name).first()


class Article(BaseModel):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText)
    content = Column(UnicodeText)
    url = Column(String)
    author = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    new_words = relationship("ArticleNewWord", backref="article")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, content, category, title=u'', author='', url=''):
        self.content = content
        self.title = title
        self.author = author
        if isinstance(category, Category):
            self.category = category
        elif isinstance(category, int):
            self.category_id = category
        else:
            raise Exception('Invalid category type: %s' % type(category))
        self.url = url

    @staticmethod
    def find_by_id(session, id):
        return session.query(Article).filter(Article.id == id).first()

    @staticmethod
    def all(session):
        return session.query(Article).all()


class Word(BaseModel):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    article_new_words = relationship("ArticleNewWord", backref="word")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, word):
        self.word = word

class ArticleNewWord(BaseModel):
    __tablename__ = 'articlenewwords'

    article_id = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    word_content = Column(String, primary_key=True)
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, article, word, word_content):
        if isinstance(article, Article):
            self.article = article
        elif isinstance(article, int):
            self.article_id = article
        else:
            raise Exception('Invalid article type: %s' % type(article))

        if isinstance(word, Word):
            self.word = word
        elif isinstance(word, int):
            self.word_id = word
        else:
            raise Exception('Invalid word type: %s' % type(word))

        self.word_content = word_content
