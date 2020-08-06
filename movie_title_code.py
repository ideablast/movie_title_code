import requests
from bs4 import BeautifulSoup
import csv

url = "https://movie.naver.com/movie/running/current.nhn"

req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, "html.parser")

cur_page = soup.find("ul", class_="lst_detail_t1")
title_list = cur_page.find_all("dt",class_ ="tit")

title_code_list = [] 

for title in title_list:
    code = title.find("a")["href"].replace("/movie/bi/mi/basic.nhn?code=","")
    #.split("code=") -> 괄호안의 문자열을 기준으로 나눠서 리스트를 리턴
    #문자열 슬라이싱을 이용 .find('code=')
    movie_title = title.find("a").get_text()
    #.contents[0] -> text를 리스트로 리턴
    title_code_list.append({ movie_title : code})

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=188909',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=X3A74U4PCIUV6; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; _gid=GA1.2.1611304192.1596617014; _ga=GA1.1.265119137.1596617014; _ga_7VKFYR6RV1=GS1.1.1596617013.1.0.1596617014.59; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; JSESSIONID=00F76AA23540FB53375F71EA73E38206; csrf_token=5c15ff3a-2f84-4b17-9c47-fb1bd3afc73a',
}

movie_reviews = []

for movie in title_code_list:
    
    params = (
        ('code', movie.values()),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    req_url = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    html = req_url.text

    soup = BeautifulSoup(html, "html.parser")
    review_list = soup.select('body > div > div > div.score_result > ul > li')

    idx = 0
    score_reple_list = []
    for  review in review_list:

        star_score_each = review.find("em").get_text()
        reple_each = ''
        
        if(review.find("span", class_="_unfold_ment") is not None):
            reple_each = review.find("a").get("data-src").strip()
        
        else:
            reple_each =review.find("span", id=f"_filtered_ment_{idx}").get_text().strip()

        score_reple_list.append([star_score_each, reple_each])
        idx += 1
    print(score_reple_list)

    # movie_review = { movie.keys() : score_reple_list }
    # movie_reviews.append(movie_review)

 
    

# for star_score in star_score_list:
#     star_score_each = star_score.find("em").get_text()

# idx = 0
# for reple in reple_list:
#     if(reple.find("span", class_="_unfold_ment") is not None):
#         reple_each = reple.find("a").get("data-src").strip()
        
#     else:
#         reple_each =reple.find("span", id=f"_filtered_ment_{idx}").get_text().strip()
#     print(reple_each)
#     idx +=1


        

    