#coding:utf8

from unittest import TestCase
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from ljn.Model import BaseModel, Category, Article, Word, ArticleNewWord

class DbTestCase(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        BaseModel.metadata.create_all(engine)
        self.session_maker = sessionmaker(engine)

    def session(self):
        return self.session_maker()


class TestCategory(DbTestCase):
    def test(self):
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


class TestArticle(DbTestCase):
    def test(self):
        s = self.session()
        c = Category(u'c1')
        a1 = Article(u'ac1', c, u'at1')
        a2 = Article(u'ac2', c, u'at2')
        s.add_all([c, a1, a2])
        s.commit()

        self.assertEqual(c, a1.category)
        self.assertEqual(c, a2.category)
        self.assertEqual(c.articles, [a1, a2])

        w1 = Word('this')
        w2 = Word('that')
        a1.new_words.append(ArticleNewWord(a1, w1, 'This'))
        a1.new_words.append(ArticleNewWord(a1, w1, 'this'))
        a1.new_words.append(ArticleNewWord(a1, w2, 'that'))
        s.commit()

        self.assertEqual(len(w1.article_new_words), 2)
        self.assertEqual(len(w2.article_new_words), 1)
