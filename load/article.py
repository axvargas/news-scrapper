'''
Created Date: Friday July 16th 2021 11:17:28 pm
Author: Andrés X. Vargas
-----
Last Modified: Friday July 23rd 2021 12:10:32 am
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
from sqlalchemy import Column, String, Integer
from base import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    body = Column(String)
    title = Column(String)
    host = Column(String)
    url = Column(String, unique=True)
    newspaper_uid = Column(String)
    n_tokens_body = Column(Integer)
    n_tokens_title = Column(Integer)

    def __init__(self,
                 uid,
                 body,
                 title,
                 host,
                 url,
                 newspaper_uid,
                 n_tokens_body,
                 n_tokens_title):
        self.id = uid
        self.body = body
        self.title = title
        self.host = host
        self.url = url
        self.newspaper_uid = newspaper_uid
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title

    
