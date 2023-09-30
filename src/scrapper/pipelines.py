from numpy import nan
from itemadapter import ItemAdapter
from scrapy import Item, Spider
from scrapy.exceptions import DropItem

class DropNotGameItemPipeline:
    def __init__(self) -> None:
        self.not_allowed_titles = ['NoPing - 30 days', 'The Crown Stones: Mirrah - DEMO']
        self.not_allowed_drm = ['Microsoft - Office']
        
    def process_item(self, item: Item, spider: Spider) -> Item:
        adapter = ItemAdapter(item)
        
        if adapter['drm'] not in self.not_allowed_drm:
            if adapter['title'] not in self.not_allowed_titles:
                spider.logger.info('Item is a game.')
                return adapter.item
        raise DropItem(f"Removing item {adapter['title']} for not be a game!")

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
        
        # Correct "release_dates" column
        for title, release_date in self.release_dates_to_correct.items():
            if adapter['title'] == title:
                adapter['release_date'] = release_date
        
        # Correct "drm" column
        for old_value, new_value in self.drms_to_correct.items():
            if adapter['drm'] == old_value:
                adapter['drm'] = new_value
        if adapter['drm'] == 'Windows':
            adapter['os'], adapter['drm'] = 'Windows', nan
        
        # Correct "os" column
        if adapter['os'] == 'Windows,Xbox Series S|X':
            adapter['os'] = 'Windows'
        
        return adapter.item

