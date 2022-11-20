import asyncio
from dataclasses import dataclass
import aiohttp
import bs4



@dataclass(frozen=True, slots=True)
class SearchResult:
    url: str
    title: str
    description: str

    @property
    def base_url(self):
        '''URL format: https://google.com'''
        return '/'.join(self.url.split('/')[:3])+'/'

    @property
    def clear_base_url(self):
        '''URL format: google.com'''
        return self.url.split('/')[2]

    


class GoogleSearch:
    SEARCH_URL = 'https://www.google.com/search'
    USR_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    TIMEOUT = aiohttp.ClientTimeout(total=10)

    __slots__ = ('_clean_query', '_num_requests', '_num_results_per_request', '_lang', '_proxy_url', '_proxy_auth', '_start')


    def __init__(
        self, 
        query: str, 
        num_requests=1,
        num_results_per_request=10,
        lang='en', 
        proxy_url: str|None=None, 
        proxy_auth: aiohttp.BasicAuth|None=None
        ) -> None:

        self._clean_query = query.replace(' ', '+')
        self._num_requests = num_requests
        self._num_results_per_request = num_results_per_request
        self._lang = lang
        self._proxy_url = proxy_url
        self._proxy_auth = proxy_auth
        self._start = 0


    def _get_params(self) -> dict[int, int|str]:
        return dict(
            q=self._clean_query,
            num = self._num_results_per_request,
            hl = self._lang,
            start = self._start * self._num_results_per_request
        )
 

    async def _make_request(self, session: aiohttp.ClientSession) -> str:
        async with session.get(
            url=self.SEARCH_URL, 
            headers=self.USR_AGENT, 
            params=self._get_params(), 
            proxy=self._proxy_url, 
            proxy_auth=self._proxy_auth
            ) as response:

            response.raise_for_status()
            return await response.text()


    def _parse_results(self, html: str) -> bs4.ResultSet:
        soup = bs4.BeautifulSoup(html, 'lxml')
        return soup.find_all('div', attrs={'class': 'g'})


    def _parse_result_data(self, result: bs4.element.Tag):
        url = result.find('a', href=True)['href']
        title = result.find('h3')
        description_box = result.find('div', {'style': '-webkit-line-clamp:2'})
        if not description_box or not url or not title:
            return None, None, None
        description = description_box.find('span')
        return url, title, description


    async def search(self):
        async with aiohttp.ClientSession(timeout=self.TIMEOUT) as session:
            while self._start < self._num_requests:
                response_html = await self._make_request(session)
                for result in self._parse_results(response_html):
                    url, title, description = self._parse_result_data(result)
                    if not url:
                        continue
                    yield SearchResult(url=url, title=title, description=description)
                self._start += 1



async def main():
    async for result in GoogleSearch(
        query='russia', 
        # proxy_url='http://111.111.111.111:8000', 
        # proxy_auth=aiohttp.BasicAuth('111111', '111111'), 
        num_results_per_request=10, 
        num_requests=2
        ).search():

        print(result.url)
        print(result.base_url)
        print(result.clear_base_url)


if __name__ == '__main__':
    asyncio.run(main()) 