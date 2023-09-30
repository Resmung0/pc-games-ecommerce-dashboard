#import re
#from io import StringIO
from typing import Iterator

#import pandas as pd
from tqdm.asyncio import trange
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http import Response
from bs4 import BeautifulSoup

from scrapper.items import NuuvemItem


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
        header = response.xpath('/html/body/div[3]/div/main/div[3]/div[5]/header')
        loader.add_value('title', header.css('h1 span ::text').get())
        loader.add_value('drm', header.css('ul li a div span  ::text').get())
        loader.add_value('os', header.xpath('ul[2]/li/a/div/span/text()').getall())
        
        # Price values
        loader.add_value('price', self.scrape_price(response))
  
        # Release date, Developer, Publisher
        rows = response.xpath('//*[@id="product"]/div[5]/div/aside[2]/div/div[1]/ul')
        rows = BeautifulSoup(rows.get(), "html.parser").find_all('li')
        rows = [
            item.get_text().split(':')[1].replace('\n', '').strip() for item in rows
        ]
        loader.add_value('release_date', rows[0])
        
        try:
            developer = rows[1]
        except IndexError as _:
            developer = '-'
        loader.add_value('developer', developer)
        
        try:
            publisher = rows[2]
        except IndexError as _:
            publisher = '-'
        loader.add_value('publisher', publisher)
        
        # Genre
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[2]/ul'
        genre = response.xpath(xpath).css('li ::text')
        loader.add_value('genre', genre.getall())
        
        # Game mode
        game_mode = self.scrape_game_mode(response)
        loader.add_value('game_mode', game_mode)
        
        # Languages  #TODO: (TERMINAR)
        # languages = response.xpath('//*[@id="product"]/div[5]/div/aside[2]/div/div[4]/table')
        # languages = pd.read_html(StringIO(languages.get()))[0].drop(0)
        # languages.columns =  ['language', 'audio', 'interface', 'subtitles']
        
        # Ratings
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[5]/ul/li/div[2]/h4/text()'
        loader.add_value('rate', response.xpath(xpath).get())
        
        # # Minimum requirements
        # xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/section[2]/section[4]/div/div[1]/div[1]/ul/li'
        # requirements = self.scrape_requirements(response, xpath, 'minimum')
        
        # # Recommended requirements
        # xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/section[2]/section[4]/div/div[1]/div[2]/ul/li'
        # requirements = self.scrape_requirements(response, xpath, 'recommended')
        return loader.load_item()
    
    def scrape_price(self, response: Response) -> str:
        price = response.xpath('/html/body/div[3]/div/main/div[3]')
        soup = BeautifulSoup(price.get(), "html.parser")
        
        product_price = 'product-price--old'
        if not product_price in price.get():
            product_price = 'product-price--val'

        price = soup.find('span', class_=product_price).get_text()
        return price.replace('\n', '')

    def scrape_game_mode(self, response: Response) -> list[str]:
        xpath = '/html/body/div[3]/div/main/div[3]/div[5]/div/aside[2]/div/div[3]/ul'
        rows = response.xpath(xpath)
        new_rows = []
        for row in rows.css('li ::text').getall():
            row = row.replace('\n', '').strip() 
            if len(row) != 0: 
                new_rows.append(row)
        return new_rows
    
    # def scrape_requirements(
    #     self,
    #     response: Response,
    #     xpath: str,
    #     requirement_type: str
    # ) -> list[dict[str, str]]:
    #     requirements = []
    #     for requirement in response.xpath(xpath):
    #         pc_info = requirement.xpath('strong/text()').get()
    #         pc_info = f'{requirement_type}_' + pc_info.replace(':', '').lower()
    #         pc_specs = requirement.xpath('span/text()').get()
    #         requirements.append({pc_info: pc_specs})
    #     return requirements
       
   