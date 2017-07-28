import lxml.html
import requests
import itertools
"""
Script for scraping this site with "developer quotes"
"""
p = requests.get("https://fortrabbit.github.io/quotes/")
t = lxml.html.fromstring(p.content)
quote_tags = t.xpath('//p[@class="type-l p-m"]')
author_tags=t.xpath('//div[@class="m-top-m"]')
with open("inspo_quotes.txt","r+") as f:
    for q,a in itertools.izip(quote_tags,author_tags):
        q_c = str(q.text_content().encode('utf-8')).strip()
        a_c = str(a.text_content().encode('utf-8')).strip()
        if len(q_c) > 0  and len(a_c) > 0:
            f.write("Quote:" + q_c + '\n') 
            f.write("Author:" + a_c + '\n')

with open("inspo_quotes.txt","r") as f:
    for line in f.readlines():
        print("Line: " + line)


