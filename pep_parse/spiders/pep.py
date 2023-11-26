import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a[href^="pep-"]')
        for pep_item in all_peps:
            yield response.follow(pep_item, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        number, name = title.split(' – ')
        yield PepParseItem(
            {
                'number': number.split()[-1],
                'name': name,
                'status': response.css(
                    'dt:contains("Status")+dd abbr::text').get(),
            }
        )
