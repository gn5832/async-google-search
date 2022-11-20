# async-google-search
async-google-search is a Python library for searching Google, easily. googlesearch uses aiohttp and BeautifulSoup4 to scrape Google. 


## usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
from asyncgooglesearch import GoogleSearch
async def main():
    async for result in GoogleSearch(query='test query').search():
        print(result.url)
```

## Additional options
googlesearch supports a few additional options. By default, googlesearch returns 10 results. This can be changed. To get a 100 results on Google for example, run the following program.
```python
async def main():
    async for result in GoogleSearch(query='test query', num_results_per_request=20, num_requests=5).search():
        print(result.url)
```
In addition, you can change the language google searches in. For example, to get results in French run the following program:
```python
async def main():
    async for result in GoogleSearch(query='test query', lang='ru').search():
        print(result.url)
```
## GoogleSearch
```python
GoogleSearch(query: str, num_requests: int = 1, num_results_per_request: int = 10, lang: str = 'en', proxy_url: str | None = None, proxy_auth: BasicAuth | None = None)
```