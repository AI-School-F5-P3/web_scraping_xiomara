import scrapy

from logger import logger
from quotescraper.items import QuoteItem, AuthorItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    authors = []

    def parse(self, response):
        quotes = response.css("div.quote")
        quote_item = QuoteItem()
        for quote in quotes:
            quote_item['quote'] = quote.css("span.text::text").get()
            quote_item['author'] = quote.css("small.author::text").get()
            quote_item['tags'] = quote.css("div.tags a.tag::text").getall()
            author_url = quote.css(("div.quote span a::attr(href)")).get()
            if author_url not in self.authors:
                logger.info(f"New author: {quote_item['author']}")
                self.authors.append(author_url)
                request = response.follow(author_url, self.parse_about, cb_kwargs=dict())
                request.cb_kwargs["author"] = quote_item['author']
                yield request
            yield quote_item
            
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            url_next = "https://quotes.toscrape.com" + next_page
            yield response.follow(url_next, callback=self.parse)

    def parse_about(self, response, author):
        author_item = AuthorItem()
        author_item['author'] = author
        author_item['about'] = response.css(".author-description::text").get()
        yield author_item

