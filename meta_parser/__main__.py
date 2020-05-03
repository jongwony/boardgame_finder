import json
import asyncio
from glob import iglob

from bs4 import BeautifulSoup


async def get_data():
    for path in iglob('data/*'):
        with open(path) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            soup._title = path
            yield soup
        await asyncio.sleep(0)


def parse(soup):
    if table := soup.find('table'):
        pairs = []
        for tr in table.find_all('tr'):
            for img in tr.select('img'):
                img_td = img.find_parent('td')
                img_td.extract()
            pair = [td.get_text(strip=True) for td in tr.find_all('td') if td.text]
            if len(pair) != 2:
                continue
            pairs.append(pair)

        if pairs:
            return dict(pairs)


async def main():
    meta = []
    async for soup in get_data():
        if parsed := parse(soup):
            parsed['게임명'] = soup._title.replace('data/', '').replace('.html', '')
            meta.append(parsed)
    with open('boardgame_meta.json', 'w') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
