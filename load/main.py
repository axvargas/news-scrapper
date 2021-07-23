'''
Created Date: Friday July 16th 2021 11:18:01 pm
Author: Andrés X. Vargas
-----
Last Modified: Friday July 23rd 2021 12:11:14 am
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import argparse
import logging
import pandas as pd

from article import Article
from base import Base, engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    articles = pd.read_csv(filename)

    for index, row in articles.iterrows():
        logger.info(f"Loading article uid {row['uid']} into DB")
        article = Article(
            row['uid'],
            row['body'],
            row['title'],
            row['host'],
            row['url'],
            row['newspaper_uid'],
            row['n_tokens_body'],
            row['n_tokens_title']
        )

        session.add(article)
    
    session.commit()
    session.close()
    logger.info("Data successfully loaded into DB")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename',
        help='The file you want to load into the db',
        type=str
    )

    args = parser.parse_args()

    main(args.filename)
