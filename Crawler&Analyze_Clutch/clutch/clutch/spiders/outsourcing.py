import scrapy

class OutsourcingSpider(scrapy.Spider):
    name = 'outsourcing'
    start_urls = ['https://clutch.co/it-services/outsourcing']

    def parse(self, response):
        items = response.xpath('//ul[@class="directory-list active"]/li')
        for item in items:
            #self.log(item.xpath('.//a/@href').extract_first())
            url = item.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_detail)
        next_page = response.xpath('//ul[contains(@class,"pagination justify-content-center")]//li[@class = "page-item next"]//a/@href').extract_first()
        if next_page:
            self.log('Próxima Pagina: {}'.format(next_page))
            yield scrapy.Request(
                url = response.urljoin(next_page),callback=self.parse
                )  
    def parse_detail(self, response):
        #self.log(response.url)
        company_name = response.xpath('//h1/a/text()').extract_first()
        min_project_size = response.xpath("//i[@data-content='Min. project size']/following-sibling::span/text()").extract_first()
        employees = response.xpath("//i[@data-content='Employees']/following-sibling::span/text()").extract_first()
        hourly_rate = response.xpath("//i[@data-content='Avg. hourly rate']/following-sibling::span/text()").extract_first()
        founded = response.xpath("//i[@data-content='Founded']/following-sibling::span/text()").extract_first()
        rating = response.xpath("//div[@class='rating-reviews']/span[@class='rating']/text()").extract_first()
        portfolio = response.xpath("//*[@id='portfolio']/div/div[2]/div[1]/div/div[2]/p/text()").extract_first()
        description = response.xpath("//*[@id='summary_description']/div[1]").extract_first()
        yield {
            'company_name':company_name,
            'min_project_size':min_project_size,
            'employees':employees,
            'hourly_rate':hourly_rate,
            'founded':founded,
            'rating':rating,
            'portfolio':portfolio,
            'description':description,
        }