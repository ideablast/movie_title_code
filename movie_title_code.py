import requests
from bs4 import BeautifulSoup, NavigableString, Tag

url = "https://movie.naver.com/movie/running/current.nhn"

req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, "html.parser")

cur_page = soup.find("ul", class_="lst_detail_t1")
title_list = cur_page.find_all("dt",class_ ="tit")

title_code_list = [] 

for title in title_list:
    code = title.find("a")["href"].replace("/movie/bi/mi/basic.nhn?code=","")
    movie_title = title.find("a").get_text()
    title_code_list.append({ movie_title : code})

print(title_code_list)