
from typing import Iterator

from tqdm.asyncio import trange
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http import Response
from bs4 import BeautifulSoup

from src.scrapper.items import NuuvemItem


class NuuvemSpider(CrawlSpider):
    name = 'nuuvem'
    allowed_domains = ['nuuvem.com']
    rules = [
        Rule(LinkExtractor(allow="/item"), callback="parse"),
    ]
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Create all links to scrape
        self.start_urls = self._create_url()
        self.logger.info(f'Created all links to scrape')

    
    def _create_url(self) -> Iterator[str]:
        """Function to create games catalog url pages.

        Yields:
            str: Url to make requests.
        """
        start_url = 'https://www.nuuvem.com/br-en/catalog/platforms/pc/types/games'
        for index in trange(1, 160, desc='Total pages to scrape'):
            url = start_url + f'/page/{index}' if index != 1 else start_url
            yield url
    
    
    def parse(self, response: Response) -> NuuvemItem:
        loader = ItemLoader(item=NuuvemItem())
        
        # Product header
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/header'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[4]/header'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[3]/header'
        header = response.xpath(xpath)
        loader.add_value('title', header.css('h1 span ::text').get())
        loader.add_value('drm', header.css('ul li a div span  ::text').get())
        loader.add_value('os', header.xpath('ul[2]/li/a/div/span/text()').getall())
        
        # Price values
        loader.add_value('price', self.scrape_price(response))
  
        # Release date, Developer, Publisher
        xpath = '//*[@id="product"]/div[5]/div/aside[2]/div/div[1]/ul'
        if len(response.xpath(xpath)) == 0:
            xpath = '//*[@id="product"]/div[4]/div/aside[2]/div/div[1]/ul'
        if len(response.xpath(xpath)) == 0:
            xpath = '//*[@id="product"]/div[3]/div/aside[2]/div/div[1]/ul'
        rows = response.xpath(xpath).get()
        rows = BeautifulSoup(rows, "html.parser").find_all('li')
        for item in rows:
            values = item.get_text().replace('\n', '').split(':')
            values = [value.strip() for value in values]
            loader.add_value(values[0].lower().replace(' ', '_'), values[1])
        
        # Genre
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[2]/ul'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[4]/div/aside[2]/div/div[2]/ul'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[3]/div/aside[2]/div/div[2]/ul'
        genre = response.xpath(xpath).css('li ::text').getall()
        loader.add_value('genre', genre)
        
        # Game mode
        game_mode = self.scrape_game_mode(response)
        loader.add_value('game_mode', game_mode)
                
        # Ratings
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[5]/ul/li/div[2]/h4/text()'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[4]/div/aside[2]/div/div[3]/ul/li/div[2]/h4/text()'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[4]/div/aside[2]/div/div[5]/ul/li/div[2]/h4/text()'
        rate = response.xpath(xpath).get()
        loader.add_value('rate', rate)
        
        return loader.load_item()
    
    def scrape_price(self, response: Response) -> str:
        price = response.xpath('/html/body/div[3]/div/main/div[3]')
        soup = BeautifulSoup(price.get(), "html.parser")
        
        product_price = 'product-price--old'
        if not product_price in price.get():
            product_price = 'product-price--val'

        price = soup.find('span', class_=product_price).get_text()
        return price.replace('\n', '').strip()

    def scrape_game_mode(self, response: Response) -> list[str]:
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[3]/ul'
        if len(response.xpath(xpath)) == 0:
            xpath = '/html/body/div[3]/div/main/div[3]/div[4]/div/aside[2]/div/div[3]/ul'
        rows = response.xpath(xpath)
        new_rows = []
        for row in rows.css('li ::text').getall():
            row = row.replace('\n', '').strip() 
            if len(row) != 0: 
                new_rows.append(row)
        return new_rows
