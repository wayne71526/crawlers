from bs4 import BeautifulSoup
import requests
import pandas as pd

r = requests.get("https://today.line.me/tw/v2/movie/chart/trending")
soup = BeautifulSoup(r.text, 'html.parser')

root_url = 'https://today.line.me'
lis = soup.find_all('li', class_="detailList-item")
data = {'rank':[], 'movie_name':[], 'English_name':[], 'movie_preview':[], 
        'long':[], 'class':[], 'limit':[], 'score':[]}

for li in lis:
    movie_pre    = root_url + li.find('a').get('href')
    movie_name   = li.find('h2', class_='detailListItem-title header header--sm header--primary header--ellipsis1').text
    English_name = li.find('h3', class_='detailListItem-engTitle header header--xs header--primary header--ellipsis1').text
    score        = li.find('span', class_='iconInfo-text text text--f text--secondary text--regular')
    long         = score.find_next('span', class_='text text--f text--secondary text--regular text--ellipsis1').text.split()[1]
    limit        = li.find('span', class_='glnBadge-text text text--fNarrow text--secondary text--regular')
    class_       = limit.find_next('span', class_='text text--f text--secondary text--regular text--ellipsis1').text
    
    data['movie_name'].append(movie_name.strip())
    data['English_name'].append(English_name.strip())
    data['movie_preview'].append(movie_pre)
    data['long'].append(long)
    data['class'].append(class_.strip())
    data['limit'].append(limit.text.strip())
    data['score'].append(float(score.text.strip()))
    
data['rank'] = list(range(1, 21))
data = pd.DataFrame(data)
data.to_excel('movie_rank.xlsx')