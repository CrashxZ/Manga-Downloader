import os
from urllib.request import FancyURLopener
from urllib.request import Request, urlopen as uReq
from bs4 import BeautifulSoup as soup


class AppURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/2007127 Firefox/2.0.0.11"


opener = AppURLopener()

name = input("Enter manga name $>")
name = name.replace(" ", "-")

os.makedirs(name,exist_ok=True)
url = "https://www.mangareader.net/" + name
print(url)

r = Request (url, headers={'User-Agent': 'Mozilla/5.0'})

client = uReq(r)
html_page = client.read()
client.close()

parsed_page = soup(html_page, "html.parser")

list_chapter = parsed_page.findAll("div", {"class": "chico_manga"})

chapterLimit = (len(list_chapter) - 5)  if (len(list_chapter) > 6) else (len(list_chapter) / 2)

print ("Total Chapters : - " +str(chapterLimit))

start = input("Enter Lower Limit  :>")
if int(start) < 1:
    start = 1

stop = input("Enter Upper Limit :>")
while int(stop) > chapterLimit:
    stop = input("(Invalid Upper Limit)Enter Upper Limit :>")

for i in range(int(start), int(stop)):
    r = Request(url + '/' + str(i), headers={'User-Agent': 'Mozilla/5.0'})
    manga_url = uReq(r)
    print("Downloading" + url + '/' + str(i))
    html_page = manga_url.read()
    manga_url.close()
    parsed_page = soup(html_page, "html.parser")
    chapter_size = parsed_page.find("div", {"id": "selectpage"}).text
    chapter_size = chapter_size.split()
    l = len(chapter_size)
    chapter_size = chapter_size[l - 1]
    print('Pages in Chapter : -'+str(chapter_size))
    os.makedirs(name + "/" + str(i))

    for j in range(1, int(chapter_size) + 1):
        r = Request(url + '/' + str(i) + '/' + str(j), headers={'User-Agent': 'Mozilla/5.0'})
        manga_url = uReq(r)
        print("Downloading Image :" + '/' + str(i) + '/' + str(j))
        html_page = manga_url.read()
        manga_url.close()
        parsed_page = soup(html_page, "html.parser")
        image = parsed_page.find("img", {"id": "img"})["src"]
        local_name = name + "/" + str(i) + "/" + str(j)
        opener.retrieve(image, local_name + ".jpg")

    print("Completed chapter : " + str(i))
