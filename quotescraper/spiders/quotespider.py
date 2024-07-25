import scrapy

from logger import logger
from quotescraper.items import QuoteItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    authors_urls = []

    def parse(self, response):
        quotes = response.css("div.quote")
        quote_item = QuoteItem()
        for quote in quotes:
            quote_item['quote'] = quote.css("span.text::text").get()
            quote_item['author'] = quote.css("small.author::text").get()
            quote_item['tags'] = quote.css("div.tags a.tag::text").getall()
            author_url = quote.css(("div.quote span a::attr(href)")).get()
            if author_url not in self.authors_urls:
                self.authors_urls.append(author_url)
            yield quote_item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            url_next = "https://quotes.toscrape.com" + next_page
            yield response.follow(url_next, callback=self.parse)
        # else:
        #     self.parse_about()

    # def parse_quote(self, response):
    #     pass

    # def parse_about(self, response):
    #     for author in self.authors_urls:
    #         url_about = self.start_urls[0] + author
    #         yield {
    #             "author": 
    #         }

