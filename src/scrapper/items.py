from scrapy import Field, Item


class NuuvemItem(Item):
    title = Field()
    drm =  Field()
    os = Field()
    price = Field()
    release_date = Field()
    developer = Field()
    publisher = Field()
    genre = Field()
    game_mode = Field()
    rate = Field()
