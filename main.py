'''
Created Date: Tuesday July 13th 2021 8:49:03 pm
Author: Andrés X. Vargas
-----
Last Modified: Thursday July 15th 2021 7:02:19 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import argparse
import logging
import re
import csv

from datetime import datetime
from requests.models import HTTPError
from urllib3.exceptions import MaxRetryError
from news_page_object import ArticlePage, HomePage
from common import config


logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)

is_well_formed_url = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _news_scraper(news_site_uid):
    host = config()["news_sites"][news_site_uid]["url"]
    logging.info(f'Begining scrapper for {host}')
    homepage = HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        if article:
            logger.info('Article fetched succesfully!')
            articles.append(article)

    _save_articles(news_site_uid, articles)
    logger.info(f'There are {len(articles)} saved')

def _save_articles(news_site_uid, articles):
    now = datetime.now().strftime('%Y_%m_%d')
    file_name = f'{news_site_uid}_{now}_articles.csv'
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(file_name, mode='w+', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for article in articles:
            row = [str(getattr(article, prop)).strip() for prop in csv_headers]
            writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
    logger.info(f'Start fetching article at {link}')
    article = None
    try:
        final_link = _build_link(host, link)
        if final_link:
            article = ArticlePage(news_site_uid, final_link)
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the article', exc_info=False)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    logger.info(f'Finished fetching article at {final_link}')
    return article


def _build_link(host, link):
    if is_well_formed_url.match(link):
        if link.startswith(host):
            return link
        return None

    elif is_root_path.match(link):
        return f'{host}{link}'

    else:
        return f'{host}/{link}'


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
