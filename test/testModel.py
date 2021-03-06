#coding:utf8

from unittest import TestCase
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from ljn.Model import BaseModel, Category, Article, Word, ArticleNewWord, init_sqlite_foreign_key

class ModelTestCase(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        init_sqlite_foreign_key(engine)
        BaseModel.metadata.create_all(engine)
        self.session_maker = sessionmaker(engine)

    def session(self):
        return self.session_maker()

    def add_2_categories(self):
        s = self.session()
        s.add(Category(u'c1'))
        s.add(Category(u'c2'))
        s.commit()

    def add_2_articles(self):
        self.add_2_categories()
        s = self.session()
        a1 = Article(u'This is content of article 1', Category.find_by_name(s, u'c1'), u'Title of c1')
        a2 = Article(u'This is content of article 2', Category.find_by_name(s, u'c2'), u'Title of c2')
        s.add_all([a1, a2])
        s.commit()


    def testCategory(self):
        s = self.session()
        s.add(Category(u'c1'))

        self.assertEqual(1, len(s.query(Category).all()))

        c = Category.find_by_name(s, u'c1')

        self.assertEqual(c.name, u'c1')
        self.assertEqual(len(c.articles), 0)

        s.commit()

        s.add(Article(u'ac', c, u'at'))
        s.commit()

        self.assertIsNotNone(c.create_date)
        self.assertEqual(len(c.articles), 1)

        s.delete(c)
        s.commit()

        self.assertEqual(len(Article.all(s)), 0)


    def testArticle(self):
        s = self.session()
        c = Category(u'c1')
        a1 = Article(u'ac1', c, u'at1')
        a2 = Article(u'ac2', c, u'at2')
        s.add_all([c, a1, a2])
        s.commit()

        self.assertEqual(c, a1.category)
        self.assertEqual(c, a2.category)
        self.assertEqual(c.articles, [a1, a2])


    def testArticleNewWord(self):
        self.add_2_articles()
        s = self.session()
        a1, a2 = Article.all(s)
        w1 = Word('this')
        w2 = Word('that')
        a1.new_words.append(ArticleNewWord(a1, w1, 'This'))
        a1.new_words.append(ArticleNewWord(a1, w1, 'this'))
        a1.new_words.append(ArticleNewWord(a1, w2, 'that'))
        s.commit()

        self.assertEqual(len(w1.article_new_words), 2)
        self.assertEqual(len(w2.article_new_words), 1)

        self.assertEqual(len(a1.new_words), 3)
        self.assertEqual(len(a2.new_words), 0)

        s.delete(a1)
        s.commit()

        self.assertEqual(len(w1.article_new_words), 0)
        self.assertEqual(len(w2.article_new_words), 0)
