from numpy import nan
from itemadapter import ItemAdapter
from scrapy import Item, Spider
from scrapy.exceptions import DropItem

class DropNotGameItemPipeline:
    def __init__(self) -> None:
        self.not_allowed_titles = [
            'NoPing - 30 days',
            'The Crown Stones: Mirrah - DEMO',
            'Tomb Raider Collection',
            
        ]
        self.not_allowed_drms = ['Microsoft - Office']
        
    def process_item(self, item: Item, spider: Spider) -> Item:
        adapter = ItemAdapter(item)
        
        if 'drm' in adapter:
            for not_allowed_drm in self.not_allowed_drms:
                if not_allowed_drm in adapter['drm']:
                    raise DropItem(f"Removing item {adapter['title']} for not be a game!")
            
        for not_allowed_title in self.not_allowed_titles:
            if not_allowed_title in adapter['title']:
                raise DropItem(f"Removing item {adapter['title']} for not be a game!")

        spider.logger.info('Item is a game.')
        return adapter.item

class DropUnavailableItemPipeline:
    def process_item(self, item: Item, spider: Spider) -> Item:
        adapter = ItemAdapter(item)
        if 'Unavailable' in adapter['price']:
            raise DropItem(f"Removing item {adapter['title']} for being unavailable!")
        return adapter.item

class CorrectItemPipeline:
    def __init__(self) -> None:
        self.release_dates_to_correct = {
            "Blade & Soul": '2016-01-19',
            "Disney Games Other-Worldly Pack": nan,
            "Minecraft: Java and Bedrock Edition": '2011-11-18',
            "Aquatico": '2023-12-01',
            "Banishers: Ghosts of New Eden": nan,
            "Gaucho and the Grassland": '2023-06-19',
            "Legends of Runeterra": '2020-04-29',
            "Shaiya": nan,
            "Aura Kingdom": '2013-12-23',
            "NECROPOLIS: BRUTAL EDITION": '2016-07-12',
            "Immortal Realms: Vampire Wars": '2020-08-28'
        }
        
        self.drms_to_correct = {
            'Steam - Free To Play': 'Steam',
            'Microsoft - Minecraft': 'Microsoft Store',
            'Epic Games Keyless': 'Epic Games'
        }
    
    def process_item(self, item: Item, spider: Spider) -> Item:
        adapter = ItemAdapter(item)
        
        # Correct "release_date" column
        for title, release_date in self.release_dates_to_correct.items():
            if title in adapter['title']:
                if 'release_date' in adapter:
                    adapter['release_date'].clear()
                    adapter['release_date'].append(release_date)
        
        # Correct "drm" column
        if 'drm' in adapter:
            for old_value, new_value in self.drms_to_correct.items():
                if old_value in adapter['drm']:
                    adapter['drm'].remove(old_value)
                    adapter['drm'].append(new_value)

            if 'Windows' in adapter['drm']:
                adapter['os'] = ['Windows']
                adapter['drm'].clear()
                adapter['drm'].append(nan)
        
        # Correct "os" column
        if 'os' in adapter:
            if 'Xbox Series S|X' in adapter['os']:
                adapter['os'].remove('Xbox Series S|X')
        
        # Correct "price" column
        price = adapter['price'][0].replace('R$', '')
        price = price.replace(',', '.').replace('Free', '0')
        adapter['price'] = [price.strip()]
        
        return adapter.item

