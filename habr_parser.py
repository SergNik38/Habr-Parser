import random
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from dateutil import parser
from slugify import slugify

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}



def habr_parser(last_page: int) -> list:
    """Parser for habr.com by categories"""
    categories = ['develop', 'admin', 'design', 'management',
                  'marketing',
                  'popsci']
    result = []
    new_result = []
    slugs = []
    for category in categories:
        for i in range(1, last_page + 1):
            url = f'https://habr.com/ru/flows/{category}/page{i}/'
            r = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            article_previews = soup.findAll('article',
                                            class_='tm-articles-list__item')
            for article_preview in article_previews:
                title = article_preview.find(
                    'a', class_='tm-article-snippet__title-link').text.strip()

                slug = str(article_preview.attrs.get('id')).strip()
                try:
                    preview_image = article_preview.find(
                        'image', class_='tm-article-snippet__lead-image').get(
                        'src')
                except BaseException:
                    preview_image = None
                preview_text = article_preview.find(
                    'div', class_='article-formatted-body')
                if not preview_image:
                    try:
                        preview_image = article_preview.find(
                            'img', class_='tm-article-snippet__lead-image').get('src')
                    except BaseException:
                        pass

                categories = ['develop', 'admin', 'design', 'management',
                              'marketing',
                              'popsci']

                article_preview_object = {
                    'title': title,
                    'slug': slugify(title),
                    'user': 1,
                    'category': random.randint(1, 4),
                    'content': preview_text.get_text(),
                    'created_at': str(parser.parse(str(datetime.now()))),
                    'img': preview_image,
                    'updated_at': str(parser.parse(str(datetime.now()))),
                    'is_published': True
                }
                result.append(article_preview_object)
    for el in result:
        if el['slug'] not in slugs:
            new_result.append(el)
            slugs.append(el['slug'])

    return new_result

