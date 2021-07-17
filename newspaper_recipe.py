'''
Created Date: Thursday July 15th 2021 10:25:37 pm
Author: Andrés X. Vargas
-----
Last Modified: Friday July 16th 2021 9:02:55 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import argparse
import logging
import pandas as pd
import hashlib
import nltk

from nltk.corpus import stopwords
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting the cleansing')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_bt_rows(df)
    df = _clean_body(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _delete_duplicates_entries(df, 'title')
    df = _drop_rows_with_missing_values(df)
    _save_data(df, filename)

    return df


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    logger.info(f'Newspaper uid detected: {newspaper_uid}')

    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Filling newspaper uid column with {newspaper_uid}')
    df['newspaper_uid'] = newspaper_uid

    return df


def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df


def _read_data(filename):
    logger.info(f'Reading file {filename}')
    return pd.read_csv(filename, encoding='utf8')


def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles = df[missing_titles_mask]['url'].str.extract(
        r'(?P<missing_titles>[^/]+)$').applymap(lambda title: title.replace('-', " ").capitalize())
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df


def _generate_uids_bt_rows(df):
    logger.info('Generating uids by rows')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids
    return df.set_index('uid')


def _clean_body(df):
    logger.info('Cleaning body from newlines')
    df['body'] = df.apply(lambda row: row['body'].replace('\n', ''), axis=1)

    return df


def _tokenize_column(df, column_name):
    logger.info(f'Tokenizing {column_name} column')
    stop_words = set(stopwords.words('spanish'))
    n_tokens = (df
                .dropna()
                .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                .apply(lambda valid_word_list: len(valid_word_list))
                )
    df['n_tokens_' + column_name] = n_tokens

    return df


def _delete_duplicates_entries(df, subset):
    logger.info('Removing duplicate rows')
    return df.drop_duplicates(subset=[subset], keep='first')


def _drop_rows_with_missing_values(df):
    logger.info('Dropping missing values')
    return df.dropna()


def _save_data(df, filename):
    clean_filename = f'clean_{filename}'
    logger.info(f'Saving data in {clean_filename}')
    df.to_csv(clean_filename)
    logger.info(f'Data successfully saved in {clean_filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename',
        help='The path to dirty data',
        type=str
    )

    args = parser.parse_args()
    df = main(args.filename)
