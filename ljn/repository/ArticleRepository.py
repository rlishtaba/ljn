#coding:utf8
from ljn.Model import Article

class ArticleRepository(object):
    def find(self, session, id):
        return session.query(Article).filter(Article.id==id).first()

    def get_all(self, session):
        return session.query(Article).all()
