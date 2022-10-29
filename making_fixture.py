from habr_parser import habr_parser
import json

categories = ['develop', 'admin', 'design', 'management', 'marketing',
              'popsci']

page = 1


def fixture_article_maker():
    """making articles fixture"""
    pk = 1
    result = []
    res = habr_parser(page)

    for article in res:
        article_fixture = {
            'model': 'mainapp.article',
            'pk': pk,
            'fields': article
        }

        result.append(article_fixture)
        pk += 1
    with open('002_articles.json', 'w') as file:
        json.dump(result, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    fixture_article_maker()
