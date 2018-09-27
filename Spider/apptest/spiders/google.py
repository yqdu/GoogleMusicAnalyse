# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from apptest.items import GoogleItem


class GoogleSpider(CrawlSpider):
    name = "google"
    allowed_domains = ["play.google.com"]
    # google play music has messy urls and the site dont has enough inner links 
    # so we need a start url list
    start_urls = [
        #'http://play.google.com/store/music',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA3lvdRAEGgUKA3lvdQ%3D%3D%3AS%3AANO1ljITltc&hl',
        'https://play.google.com/store/music/collection/topselling_paid_track',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAWYQBBoDCgFm:S:ANO1ljIwepw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmxvbmVseRAEGggKBmxvbmVseQ%3D%3D:S:ANO1ljJyAuM',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmFsd2F5cxAEGggKBmFsd2F5cw%3D%3D:S:ANO1ljI-0S8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWFkb3JlEAQaBwoFYWRvcmU%3D:S:ANO1ljIx5tQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgwKAmFpEAQaBAoCYWk%3D:S:ANO1ljLaXFo',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWFmdGVyEAQaBwoFYWZ0ZXI%3D:S:ANO1ljISgYM',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWFmdGVyEAQaBwoFYWZ0ZXI%3D:S:ANO1ljISgYM',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWFsb25lEAQaBwoFYWxvbmU%3D:S:ANO1ljI1HU8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhoKCWF0dGVudGlvbhAEGgsKCWF0dGVudGlvbg%3D%3D:S:ANO1ljIUnYA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJhbmcQBBoGCgRiYW5n:S:ANO1ljKgOmI',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJhYnkQBBoGCgRiYWJ5:S:ANO1ljKEq0Q',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJhY2sQBBoGCgRiYWNr:S:ANO1ljLka6Y',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2JhZBAEGgUKA2JhZA%3D%3D:S:ANO1ljI0HtI',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmJhbGFkYRAEGggKBmJhbGFkYQ%3D%3D:S:ANO1ljKAwMo',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgwKAmJlEAQaBAoCYmU%3D:S:ANO1ljLCC4Q',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhoKCWJlYXV0aWZ1bBAEGgsKCWJlYXV0aWZ1bA%3D%3D:S:ANO1ljJijSk',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmJlZ2dpbhAEGggKBmJlZ2dpbg%3D%3D:S:ANO1ljIELvw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmJldHRlchAEGggKBmJldHRlcg%3D%3D:S:ANO1ljJNhmw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2JpZxAEGgUKA2JpZw%3D%3D:S:ANO1ljKx0F8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJpbmcQBBoGCgRiaW5n:S:ANO1ljI-Hz4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWJsYWNrEAQaBwoFYmxhY2s%3D:S:ANO1ljKOVg4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB2JsZW5kZWQQBBoJCgdibGVuZGVk:S:ANO1ljKUdAQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJvZHkQBBoGCgRib2R5:S:ANO1ljKCS8U',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJvcm4QBBoGCgRib3Ju:S:ANO1ljILumw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGJvdGgQBBoGCgRib3Ro:S:ANO1ljIBXH4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWJyYXZlEAQaBwoFYnJhdmU%3D:S:ANO1ljKK7Dg',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCGJyZWFraW5nEAQaCgoIYnJlYWtpbmc%3D:S:ANO1ljKZNi4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmJyaWdodBAEGggKBmJyaWdodA%3D%3D:S:ANO1ljLJOSg',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWJyaW5nEAQaBwoFYnJpbmc%3D:S:ANO1ljIcGvw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgwKAmJ5EAQaBAoCYnk%3D:S:ANO1ljIrB_A',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2JpZxAEGgUKA2JpZw%3D%3D:S:ANO1ljKx0F8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNvbWUQBBoGCgRjb21l:S:ANO1ljKDK8I',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWNyYXp5EAQaBwoFY3Jhenk%3D:S:ANO1ljKF7Xc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNha2UQBBoGCgRjYWtl:S:ANO1ljLOZpM',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhwKCmNhbGlmb3JuaWEQBBoMCgpjYWxpZm9ybmlh:S:ANO1ljIuKMc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2NhbhAEGgUKA2Nhbg%3D%3D:S:ANO1ljI6Ufg',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNhdmUQBBoGCgRjYXZl:S:ANO1ljIMu1c',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhoKCWNob2NvbGF0ZRAEGgsKCWNob2NvbGF0ZQ%3D%3D:S:ANO1ljLG46Y',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNpdHkQBBoGCgRjaXR5:S:ANO1ljJsV04',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWNsb3NlEAQaBwoFY2xvc2U%3D:S:ANO1ljKnwpM',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNvbGQQBBoGCgRjb2xk:S:ANO1ljI-Tp4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBmNvbWluZxAEGggKBmNvbWluZw%3D%3D:S:ANO1ljJvTro',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGNvb2wQBBoGCgRjb29s:S:ANO1ljLUU90',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWNyYXNoEAQaBwoFY3Jhc2g%3D:S:ANO1ljJSFfQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWNyYXp5EAQaBwoFY3Jhenk%3D:S:ANO1ljKF7Xc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2N1dBAEGgUKA2N1dA%3D%3D:S:ANO1ljJ2ldg',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBWN1cGlkEAQaBwoFY3VwaWQ%3D:S:ANO1ljJKE58',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB2RhbmNpbmcQBBoJCgdkYW5jaW5n:S:ANO1ljIqJNQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhoKCWRhbmdlcm91cxAEGgsKCWRhbmdlcm91cw%3D%3D:S:ANO1ljLD9h8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGRhcmUQBBoGCgRkYXJl:S:ANO1ljKB6-k',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGRhcmsQBBoGCgRkYXJr:S:ANO1ljKokR4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA2RhdBAEGgUKA2RhdA%3D%3D:S:ANO1ljI8GKA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCGRpYW1vbmRzEAQaCgoIZGlhbW9uZHM%3D:S:ANO1ljJYxAc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXoQBBoDCgF6:S:ANO1ljIh-go',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXkQBBoDCgF5:S:ANO1ljIYRgI',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXgQBBoDCgF4:S:ANO1ljKB8IQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXcQBBoDCgF3:S:ANO1ljJMqH8',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXYQBBoDCgF2:S:ANO1ljLw84Y',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXUQBBoDCgF1:S:ANO1ljLX5wo',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXQQBBoDCgF0:S:ANO1ljIi4ZQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXMQBBoDCgFz:S:ANO1ljLVyYY',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXIQBBoDCgFy:S:ANO1ljKkRMU',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXEQBBoDCgFx:S:ANO1ljJ0dxY',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXAQBBoDCgFw:S:ANO1ljJoX2M',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAW8QBBoDCgFv:S:ANO1ljJcudg',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAW4QBBoDCgFu:S:ANO1ljLSA78',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCG5lZ2F0aXZlEAQaCgoIbmVnYXRpdmU%3D:S:ANO1ljKzntU',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB25lZ2xlY3QQBBoJCgduZWdsZWN0:S:ANO1ljL9xpU',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBm5hdHVyZRAEGggKBm5hdHVyZQ%3D%3D:S:ANO1ljIDagA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCG1hdGVyaWFsEAQaCgoIbWF0ZXJpYWw%3D:S:ANO1ljInC_E',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBm1hc3RlchAEGggKBm1hc3Rlcg%3D%3D:S:ANO1ljKbRqk',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBG1lYW4QBBoGCgRtZWFu:S:ANO1ljIhU6g',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBW1ham9yEAQaBwoFbWFqb3I%3D:S:ANO1ljLUqFw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBW1hdGNoEAQaBwoFbWF0Y2g%3D:S:ANO1ljLskA0',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCG9yaWdpbmFsEAQaCgoIb3JpZ2luYWw%3D:S:ANO1ljIxSf0',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCG9wcG9zaXRlEAQaCgoIb3Bwb3NpdGU%3D:S:ANO1ljIb7vQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBW9yZGVyEAQaBwoFb3JkZXI%3D:S:ANO1ljLTQiA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB3Byb2Nlc3MQBBoJCgdwcm9jZXNz:S:ANO1ljKmGZA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCHByb3BlcnR5EAQaCgoIcHJvcGVydHk%3D:S:ANO1ljKYVBI',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBnBlcmlvZBAEGggKBnBlcmlvZA%3D%3D:S:ANO1ljLrmUs',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB3F1YWxpdHkQBBoJCgdxdWFsaXR5:S:ANO1ljLqya4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB3F1YXJ0ZXIQBBoJCgdxdWFydGVy:S:ANO1ljKgbmw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB3F1YXJyZWwQBBoJCgdxdWFycmVs:S:ANO1ljJYdjw',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXNjYWxlEAQaBwoFc2NhbGU%3D:S:ANO1ljL8jYI',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBnN0YXR1cxAEGggKBnN0YXR1cw%3D%3D:S:ANO1ljLbuzA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCHNjaGVkdWxlEAQaCgoIc2NoZWR1bGU%3D:S:ANO1ljJdqX4',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXRyYWNrEAQaBwoFdHJhY2s%3D:S:ANO1ljJCipA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXRvdWdoEAQaBwoFdG91Z2g%3D:S:ANO1ljJPlB0',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhgKCHRyZWFzdXJlEAQaCgoIdHJlYXN1cmU%3D:S:ANO1ljJnCV0',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXRyZWF0EAQaBwoFdHJlYXQ%3D:S:ANO1ljJje20',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBnVyZ2VudBAEGggKBnVyZ2VudA%3D%3D:S:ANO1ljIdZbA',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBnZvbHVtZRAEGggKBnZvbHVtZQ%3D%3D:S:ANO1ljJCzJE',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhYKB3doZXJlYXMQBBoJCgd3aGVyZWFz:S:ANO1ljKW5IE',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBndvbmRlchAEGggKBndvbmRlcg%3D%3D:S:ANO1ljKeiVY',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBHdlYXIQBBoGCgR3ZWFy:S:ANO1ljIXZ4k',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBHhib3gQBBoGCgR4Ym94:S:ANO1ljIEDXc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXlpZWxkEAQaBwoFeWllbGQ%3D:S:ANO1ljKsMU0',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA3lvdRAEGgUKA3lvdQ%3D%3D:S:ANO1ljITltc',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBHlhcmQQBBoGCgR5YXJk:S:ANO1ljK4RFE',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXlhY2h0EAQaBwoFeWFjaHQ%3D:S:ANO1ljIoEJk',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhIKBXplYnJhEAQaBwoFemVicmE%3D:S:ANO1ljK8d5Q',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA3ppcBAEGgUKA3ppcA%3D%3D:S:ANO1ljLC7FQ',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=Yg4KA3pvbxAEGgUKA3pvbw%3D%3D:S:ANO1ljJQt84',
        'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhQKBnpvbWJpZRAEGggKBnpvbWJpZQ%3D%3D:S:ANO1ljLrZds',

        #'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAWUQBBoDCgFl:S:ANO1ljLP5gM',
        #'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXEQBBoDCgFx:S:ANO1ljJ0dxY',
        #'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAWoQBBoDCgFq:S:ANO1ljL9Ixk',
        #'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YgoKAXAQBBoDCgFw:S:ANO1ljJoX2M',
        #'https://play.google.com/store/music/collection/5:search_cluster:4?clp=YhAKBGxvdmUQBBoGCgRsb3Zl:S:ANO1ljKVirQ',
        #'https://play.google.com/store/music/album/Kendrick_Lamar_DAMN?id=Bwj4cpxbxjnarequw2jkj5c3a5u'
        'https: // play.google.com / store / music / album?id = Bjr3qw22vpqdmo73uctklrjpe5i'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/music/album",)), callback='parse_app', follow=True),
    ]  # CrawlSpider will proceed under given rules
    rvnum2=""
    p=re.compile("music/(album\?)id")#check is single song
    p1 = re.compile("\d\d\d\d")
    pd=re.compile("(\d:\d)")
    pp=re.compile("\$(\d+.\d)")

# to filter the data
#Url, Name, category, Review_number, Rating, Price, Duration, Released, Labe, Tracks
    def parse_app(self, response):
        item = GoogleItem()

        myurl=response.url
        value=self.p.findall(myurl)#check is single song
        #if(len(value)==0):
        #    return
        item['Url'] = myurl
        rvnum=response.xpath("//span[@class='reviews-num']").xpath("text()").extract()
        item["Rating"] = response.xpath("//div[@class='score']").xpath("text()").extract()
        MyPrice=response.xpath(
            '//button[@class="price buy id-track-click id-track-impression"]/span[2]').xpath(
            "text()").extract()
        if(len(MyPrice)==0):
            MyPrice={"$0.0"}
        firstPrice=self.pp.findall(MyPrice[0])
        item["Price"] =firstPrice[0]
        myDuration= response.xpath("//div[@class='duration']").xpath("text()").extract()
        if(len(myDuration)==0):
            return
       # myfrist=self.pd.findall(myurl)
        item['Duration'] =myDuration[0]
        #if(rvnum==self.rvnum2):
         #   return
        item["Review_number"]=rvnum
        #item["Review_number"] = response.xpath("//span[@class='reviews-num']").xpath("text()").extract()
        ctg= response.xpath("//span[@itemprop='genre']").xpath("text()").extract()
        if(len(ctg)==0 or len(ctg)>100):
            return
        #songName=response.xpath("//div[@class='title' and @tabindex='0']").xpath("text()").extract()
        songName = response.xpath("//title[@id='main-title']").xpath("text()").extract()
        item["Name"] = songName[0]
        item['category'] = ctg
        content = response.xpath("//div[@class='meta-info']").xpath("./div[@class='content']").xpath("text()").extract()
        item['Released'] = self.p1.findall(content[len(content) - 2])
        item['Label'] = re.split('\d\d\d\d', content[len(content) - 1])[1]
        myTracks=response.xpath("//div[@class='track-number has-preview']").xpath("text()").extract()
        item['Tracks']= myTracks[len(myTracks)-1]
        #item['Duration'] = response.xpath("//div[@class='duration']").xpath("text()").extract()
        self.rvnum2=rvnum
        yield item