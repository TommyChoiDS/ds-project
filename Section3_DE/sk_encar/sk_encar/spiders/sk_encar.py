import scrapy
import json
from ..items import SkEncarItem

class SkEncarSpider(scrapy.Spider):
    name = 'sk_encar'
    # allowed_domains = ['www.encar.com']
    allowed_domains = ['http://api.encar.com']
    
    start_urls = [f'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y._.Category.%EA%B2%BD%EC%B0%A8.)&sr=%7CModifiedDate%7C{i}%7C200' for i in range(0,2000,200)]
    # f'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y.)&sr=%7CModifiedDate%7C{i}%7C200'


    def parse(self, response):
        jsonresponse = json.loads(response.text)
        for car_info in jsonresponse['SearchResults']:
            item = SkEncarItem()
            item['Manufacturer'] = car_info['Manufacturer']
            item['Model'] = car_info['Model']
            item['Km'] = car_info['Mileage']
            item['Fuel'] = car_info['FuelType']
            item['Loc'] = car_info['OfficeCityState']
            item['Price'] = car_info['Price']
            item['Old_year'] = car_info['FormYear']
            item['Old_month'] = str(int(car_info['Year']))[4:]

            yield item

        # return item
