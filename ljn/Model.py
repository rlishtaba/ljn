#coding:utf8

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UnicodeText, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

BaseModel = declarative_base()

def init_sqlite_foreign_key(engine):
    def enable_foreign_key(conn, *args):
        conn.execute('PRAGMA foreign_keys=ON')

    from sqlalchemy.event import listen
    listen(engine, 'connect', enable_foreign_key)


def init():
    from os.path import join
    from g import DATA_DIR
    from sqlalchemy import create_engine

    DB_FILE = join(DATA_DIR, 'ljn.db')
    BaseModel.metadata.bind = engine = create_engine('sqlite:///' + DB_FILE.replace('\\', '/'), echo=True)
    init_sqlite_foreign_key(engine)

    BaseModel.metadata.create_all()


class Category(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    articles = relationship("Article", cascade="all,delete", backref="category")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def all(session):
        """ @rtype: list of Category """
        return session.query(Category).order_by(Category.name).all()

    @staticmethod
    def find_by_name(session, name):
        """ @rtype: Category """
        return session.query(Category).filter(Category.name == name).first()

    @staticmethod
    def find_by_id(session, id):
        """ @rtype: Category """
        return session.query(Category).filter(Category.id == id).first()


class Article(BaseModel):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText)
    content = Column(UnicodeText)
    url = Column(String)
    author = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    new_words = relationship("ArticleNewWord", cascade="all,delete", backref="article")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, content, category, title=u'', author='', url=''):
        self.content = content
        self.title = title
        self.author = author
        if isinstance(category, Category):
            self.category = category
        elif isinstance(category, int):
            self.category_id = category
        elif category is not None:
            raise Exception('Invalid category type: %s' % type(category))
        self.url = url

    @staticmethod
    def find_by_id(session, id):
        """ @rtype: Article """
        return session.query(Article).filter(Article.id == id).first()

    @staticmethod
    def all(session):
        """ @rtype: list of Article """
        return session.query(Article).all()


class Word(BaseModel):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    article_new_words = relationship("ArticleNewWord", cascade="all,delete", backref="word")
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, word):
        self.word = word

    @staticmethod
    def find(session, word):
        """ @rtype: Word """
        return session.query(Word).filter(Word.word == word).first()


class ArticleNewWord(BaseModel):
    __tablename__ = 'articlenewwords'

    article_id = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    word_content = Column(String, primary_key=True)
    create_date = Column(DateTime, default=datetime.now)

    def __init__(self, article, word, word_content):
        if isinstance(article, Article):
            self.article = article
        elif isinstance(article, int):
            self.article_id = article
        elif article is not None:
            raise Exception('Invalid article type: %s' % type(article))

        if isinstance(word, Word):
            self.word = word
        elif isinstance(word, int):
            self.word_id = word
        elif word is not None:
            raise Exception('Invalid word type: %s' % type(word))

        self.word_content = word_content

    @staticmethod
    def find_by_article_word(session, article_id, word_content):
        """ @rtype: ArticleNewWord """
        query = session.query(ArticleNewWord).filter(ArticleNewWord.article_id == article_id)
        return query.filter(ArticleNewWord.word_content == word_content).first()
