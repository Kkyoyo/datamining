import requests
import urllib
from bs4 import BeautifulSoup
import lxml
import os
import threading
import json

thread_lock = threading.BoundedSemaphore(value=10)

def page_from_url(url):
    html = requests.get(url).content.decode('utf-8')
    return html



def page_from_label(label):
    pages=[]
    C_label = urllib.parse.quote(label)
    url = 'http://home.meishichina.com/search/{}/page/{}/'
    for index in range(1,20):
        new_url=url.format(C_label,index)
        html = page_from_url(new_url)
        soup = BeautifulSoup(html, 'lxml')
        links = [link.find('a')['href'] for link in soup.find_all('div', class_='pic')]
        pages.append(links)
    return pages

def find_in_page(page,startpart,endpart):
    image_url=[]
    end=0
    while page.find(startpart,end)!=-1:
        start=page.find(startpart,end)+len(startpart)
        end=page.find(endpart,start)
        if end<0:
            break
        string=page[start:end]
        end=end+len(endpart)
        image_url.append(string)
    return image_url


def download_txt(url,label,n):
    html = page_from_url(url)
    print('正在下载第'+str(n)+'个菜谱')
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('div', class_="recipe_De_imgBox").find('a')['title']
    text = [index for index in soup.find_all('div', class_='recipeStep_word')]
    steps = find_in_page(str(text), '</div>', '。</div>')
    path = 'meishi/' + str(label) + '/' + str(title) +str(n)+ '.txt'
    with open(path, 'w',encoding='utf-8') as f:
        for step in steps:
            f.write(step + '\n')
        f.write(url)

def main(label):
    links = page_from_label(label)
    n=0
    for pages in links:
        for meishi_url in pages:
            if hasNumbers(meishi_url):
                n += 1
                download_txt(meishi_url, label, n)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# url='http://home.meishichina.com/recipe-16872.html'
label = '牛肉'
if __name__=='__main__':
    if os.path.exists('d:/pytest2/meishi/'+str(label))==0:
        os.makedirs('meishi/'+str(label))
    main(label)
# download_txt(url,label,n=2)








#
# label='鸡蛋'
# url='http://home.meishichina.com/recipe-30617.html'
# html=page_from_url(url)
# soup = BeautifulSoup(html,'lxml')
# title=soup.find('div',class_="recipe_De_imgBox").find('a')['title']
# text=[index for index in soup.find_all('div',class_='recipeStep_word')]
#
# steps = find_in_page(str(text),'</div>','。</div>')
# path = 'meishi/' +str(label)+'/'+ str(title)+'.txt'
# os.makedirs('meishi//'+str(label))
# with open(path, 'w') as f:
#     for step in steps:
#         f.write(step+'\n')
# # print(text)
# print(title)

