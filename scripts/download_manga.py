import requests
import string
import os
import errno
from bs4 import BeautifulSoup

from urllib.parse import urlparse


headers = {
    'Referer': 'https://mangakakalot.com/'
}


def get_page_response(url):
    return requests.get(url, headers=headers).text


def get_page_response_b(url):
    return requests.get(url, headers=headers).content


def validate_string(s):
    invalids = '#%&{}\\/<>*?$!\'":@+`|='
    valids = '＃％＆｛｝＼／＜＞＊？＄！’”：＠＋｀｜＝'

    res = []
    for c in s:
        if c == ' ':
            res.append(c)
        elif c in string.whitespace:
            continue
        elif c in invalids:
            pos = invalids.find(c)
            res.append(valids[pos])
        else:
            res.append(c)

    return ''.join(res)


def download_content(url, path):
    img_data = get_page_response_b(url)

    filedir = os.path.dirname(path)
    if not os.path.exists(filedir):
        try:
            os.makedirs(filedir)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(path, 'wb') as handler:
        handler.write(img_data)


def get_image_name(url):
    return urlparse(url).path.split('/')[-1]


def get_manga_data(url):
    html = get_page_response(url)
    soup = BeautifulSoup(html, 'html.parser')

    chapters = []
    selector = soup.select('div.chapter-list div.row span a')
    selector.reverse()
    for i, chapter in enumerate(selector):
        chapternum = str(i).zfill(3)
        name = chapter.text
        name = f'{chapternum} - {name}'
        url = chapter.attrs['href']

        res = {'name': name, 'url': url}
        chapters.append(res)

    name = soup.select('.manga-info-text h1')[0].text

    # {name, chapters: {name, url}}
    manga = {'name': name, 'chapters': chapters}
    return manga


def get_chapter_data(url):
    html = get_page_response(url)
    soup = BeautifulSoup(html, 'html.parser')

    pages = []
    selector = soup.select('div.container-chapter-reader img')
    for i, page in enumerate(selector):
        url = page.attrs['src']
        pagenum = str(i).zfill(3)
        name = get_image_name(url)
        name = f'{pagenum} - {name}'

        res = {'name': name, 'url': url}
        pages.append(res)

    #{pages: {name, url}}
    chapter = {'pages': pages}
    return chapter


def download_manga(url, path):
    manga = get_manga_data(url)
    mname = validate_string(manga['name'])
    mpath = os.path.join(path, mname)

    for chapter in manga['chapters']:
        cname = validate_string(chapter['name'])
        cpath = os.path.join(mpath, cname)
        cdata = get_chapter_data(chapter['url'])

        for page in cdata['pages']:
            print(f'Downloading {page["url"]}')

            pname = validate_string(page['name'])
            ppath = os.path.join(cpath, pname)
            download_content(page['url'], ppath)


if __name__ == '__main__':
    url = 'https://mangakakalot.com/manga/manga-url-here'
    path = './mangas'
    download_manga(url, path)
