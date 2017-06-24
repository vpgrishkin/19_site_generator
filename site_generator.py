import os
import json
import copy

from jinja2 import Environment, FileSystemLoader
import markdown


OUTPUT_SITE_PATH = 'site'
ARTICLES_PATH = 'articles'
TEMPLATES_PATH = 'templates'
INDEX_FILE = 'index.html'
CONFIG = 'config.json'
ENCODING = 'utf-8'


def load_file(file_path, default_encoding):
    with open(file_path, encoding=default_encoding) as file:
        return file.read()


def get_jinja_template(filename, path):
    env = Environment(loader=FileSystemLoader(path),
                      auto_reload=True,
                      trim_blocks=True,
                      lstrip_blocks=True,)
    return env.get_template(filename)


def add_source_html(articles):
    articles_source_html = copy.deepcopy(articles)
    for article in articles_source_html:
        article['source_html'] = article['source'].replace('.md', '.html')
    return articles_source_html


def write_html_articles(articles, article_template, article_path, default_encoding, site_path):
    for article in articles:
        md_article_path = os.path.join(article_path, article['source'])
        content = markdown.markdown(load_file(md_article_path, default_encoding))
        article_html = article_template.render(content=content,
                                               title=article['title'])
        html_article_path = os.path.join(site_path, article['source_html'])
        html_article_dir = os.path.dirname(html_article_path)

        if not os.path.exists(html_article_dir):
            os.makedirs(html_article_dir)

        write_html_file(html_article_path, article_html, default_encoding)


def write_html_file(path, article_html, default_encoding):
    with open(path, 'w', encoding=default_encoding) as html_file:
        html_file.write(article_html)


if __name__ == '__main__':
    config = json.loads(load_file(CONFIG, ENCODING))
    articles = config['articles']
    topics = config['topics']
    article_template = get_jinja_template('article.html', TEMPLATES_PATH)
    articles_source_html = add_source_html(articles)
    write_html_articles(articles_source_html,
                        article_template,
                        ARTICLES_PATH,
                        ENCODING,
                        OUTPUT_SITE_PATH)
    index_template = get_jinja_template('index.html', TEMPLATES_PATH)
    index_html_content = index_template.render(topics=topics,
                                               articles=articles_source_html)
    index_html_path = os.path.join(OUTPUT_SITE_PATH, 'index.html')
    write_html_file(index_html_path, index_html_content, ENCODING)
