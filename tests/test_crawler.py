from os.path import join
from dataclasses import dataclass
from unittest.mock import patch

from requests import Session

from crawler.__main__ import NamuWiki


@dataclass()
class MockResponse:
    content: bytes


def new_get(*args, **kwargs):
    with open(join('tests', 'samples', 'namu_boardgame_list.html'), 'rb') as f:
        content = f.read()
    return MockResponse(content)


def test_pagination():
    with patch.object(Session, 'get', new=new_get):
        crawler = NamuWiki()
        crawler.fetch()
        assert crawler.next_elem().attrs['href'] == '/w/%EB%B6%84%EB%A5%98:%EB%B3%B4%EB%93%9C%20%EA%B2%8C%EC%9E%84?namespace=%EB%AC%B8%EC%84%9C&cfrom=%EB%A0%88%EC%A0%84%EB%8D%94%EB%A6%AC'


def test_get_list():
    with patch.object(Session, 'get', new=new_get):
        crawler = NamuWiki()
        crawler.fetch()
        assert next(crawler.get_list()).text == '100% 오렌지 주스'
