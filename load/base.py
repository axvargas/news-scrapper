'''
Created Date: Friday July 16th 2021 11:17:53 pm
Author: Andrés X. Vargas
-----
Last Modified: Thursday July 22nd 2021 11:16:02 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

engine = create_engine('sqlite:///newspapaer.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()
