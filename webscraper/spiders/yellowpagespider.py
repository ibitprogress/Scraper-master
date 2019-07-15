import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class YellowPagesSpider(CrawlSpider):
    name = "yp"
    start_urls = [
        "https://www.yellowpages.com/austin-tx/plumbers",
        
    ]
    rules = (
        Rule(LinkExtractor(allow=('page=\d+',)), callback='parse_page'),
    )

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):

        for item in response.css('div.result'):
            links = item.css('div.links')
            links = re.sub(r'\<[^>]*\>', '', str(links.extract()))
            title = item.css('div.info>h2.n')
            title = re.sub(r'\<[^>]*\>', '', str(title.extract()[0]))
            if "Directions" in links and title[0].isdigit():
                phone = item.css('div.phones')
                try:
                    phone = re.sub(r'\<[^>]*\>', '', str(phone.extract()[0]))
                    phone = re.findall(r'[0-9]',phone)
                    phone = ''.join(phone)
                    street = item.css("div.street-address")
                    location = item.css('div.locality')
                    street = re.sub(r'\<[^>]*\>', '', str(street.extract()[0]))
                    location = re.sub(r'\<[^>]*\>', '', str(location.extract()[0]))
                    location = street + location
                except:
                    pnone = ""
                title = re.sub(r'[0-9.]','', title)

                title = title.replace('\u00a0','')
                scraped_data = {
                    title : {
                    'phone': phone,
                    'location':location,
                    }
                }
                yield scraped_data
