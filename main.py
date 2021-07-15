'''
Created Date: Tuesday July 13th 2021 8:49:03 pm
Author: Andrés X. Vargas
-----
Last Modified: Tuesday July 13th 2021 10:21:10 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import argparse
import logging
from common import config


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()["news_sites"][news_site_uid]["url"]
    logging.info(f'Begining scrapper for {host}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    news_sites_choices = list(config()['news_sites'])
    parser.add_argument(
        'news_site',
        help='The news site you want to scrape',
        type=str,
        choices=news_sites_choices
    )

    args = parser.parse_args()
    _news_scraper(args.news_site)
