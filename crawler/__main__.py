import asyncio
import re
from os.path import join, exists

import aiohttp
from bs4 import BeautifulSoup
from requests import Session


class NamuWiki(Session):
    def __init__(self):
        super().__init__()
        self.domain = 'https://namu.wiki'
        self.url = f'{self.domain}/w/%EB%B6%84%EB%A5%98:%EB%B3%B4%EB%93%9C%20%EA%B2%8C%EC%9E%84'
        self.soup = None

    def set_url(self, path):
        self.url = f'{self.domain}{path}'

    def fetch(self):
        resp = self.get(self.url)
        self.soup = BeautifulSoup(resp.content, 'html.parser')

    def next_elem(self):
        return self.soup.find(text=re.compile('Next')).parent

    def get_list(self):
        next_elem = self.next_elem()
        div = next_elem.find_next('div')
        yield from div.select('a')


async def get_link(crawler):
    crawler.fetch()
    next_elem = crawler.next_elem()
    while True:
        print(crawler.url)
        for a in crawler.get_list():
            yield dict(a.attrs, title=a.text)
            await asyncio.sleep(0)
        if href := next_elem.attrs.get('href'):
            crawler.set_url(href)
            next_elem = crawler.next_elem()
            crawler.fetch()
        else:
            break


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    crawler = NamuWiki()
    async with aiohttp.ClientSession() as session:
        async for a in get_link(crawler):
            target = join('data', a['title'].replace('/', '_') + '.html')
            if not exists(target):
                print(target)
                html = await fetch(session, f"{crawler.domain}{a['href']}")
                assert '비정상적인 트래픽 감지' not in html
                with open(target, 'w') as f:
                    f.write(html)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
