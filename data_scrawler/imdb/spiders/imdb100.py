import scrapy
import re

class Imdb100Spider(scrapy.Spider):
    global time
    name = 'imdb100'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/search/title/']
    time = 2021

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31&sort=num_votes,desc&count=100', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        })

    def roll_back_date(self, chart_year):
        chart_year -= 1
        return chart_year

    def parse(self, response):
        for i in range(0, 100):
            try:
                time = response.xpath("//span[starts-with(@class, 'lister-item-year text-muted unbold')]/text()")[i].get()[1:-1]
                if len(time) == 4:
                    time = int(time)
                    break
            except:
                pass
        for i in range(0, 100):
            try:
                item = response.xpath("//div[starts-with(@class, 'lister-item-content')]")[i].get()
            except:
                item = None
            try:
                title = response.xpath("//a[starts-with(@href, '/title')]/text()")[3 * i + 2].get()
            except:
                title = None  
            try:               
                year = response.xpath("//span[starts-with(@class, 'lister-item-year text-muted unbold')]/text()")[i].get()
            except:
                year = None 
            try:
                genre = response.xpath("//span[starts-with(@class, 'genre')]/text()")[i].get().strip()
            except:
                genre = None   
            try:
                runtime = response.xpath("//span[starts-with(@class, 'runtime')]/text()")[i].get().strip()
            except:
                runtime = None   
            try:
                certificate = response.xpath("//span[starts-with(@class, 'certificate')]/text()")[i].get()
            except:
                certificate = None  
            try:
                rating = float(response.xpath("//strong/text()")[i + 2].get())
            except:
                rating = None  
            try:
                imdb_id = response.xpath("//span[starts-with(@class, 'userRatingValue')]")[i].get().split('\n')[0].split('"')[-2]
            except:
                imdb_id = None 
            try:
                description = response.xpath("//p[starts-with(@class, 'text-muted')]/text()")[7 * i + 6].get().strip()
            except:
                description = None 
            try:
                meta_score = int(response.xpath("//span[starts-with(@class, 'metascore  favorable')]/text()")[i].get().strip())
            except:
                meta_score = None  
            try:
                director = re.findall(r'>.*<', item.split('Director')[1].split('Star')[0].split('ghost')[0])
                for n in range(len(director)):
                    director[n] = director[n][1:-1]
            except:
                director = None  
            try:
                director_id = re.findall(r'/name/.*/">', item.split('Director')[1].split('Star')[0])
                for n in range(len(director_id)):
                    director_id[n] = director_id[n][6:-4]
                # director_id = str(director_id)
            except:
                director_id = None
            try:
                star = re.findall(r'>.*<', item.split('Star')[1].split('Votes:')[0])
                for n in range(len(star)):
                    star[n] = star[n][1:-1]
            except:
                star = None    
            try:
                star_id = re.findall(r'/name/.*/">', item.split('Star')[1])
                for n in range(len(star_id)):
                    star_id[n] = star_id[n][6:-4]
                # star_id = star_id
            except:
                star_id = None        
            try:
                num_votes = item.split('Votes')[1].split('</span>')[1].split('>')[1].replace(",", "")
            except:
                num_votes = None   
            try:                         
                gross = int(re.findall(r'data-value=".*"', item.split('Gross')[1].split('$')[0])[0][12:-1].replace(",", ""))
            except:
                gross = None           
            yield {
                'title': title,
                'year': year[1:-1],
                'genre': genre,
                'runtime': runtime,
                'certificate': certificate,
                'rating': rating,
                'imdb_id': imdb_id,
                'description': description,
                'meta_score': meta_score,
                'director': director,
                'director_id': director_id,
                'star': star,
                'star_id': star_id,
                'num_votes': num_votes,
                'gross': gross
            }
        time = self.roll_back_date(time)
        
        if time < 2018:
            return
        else:
            next_page_url = f'https://www.imdb.com/search/title/?release_date={str(time)}-01-01,{str(time)}-12-31&sort=num_votes,desc&count=100'
            yield scrapy.Request(next_page_url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
            })
            