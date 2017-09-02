import os
from urllib.request import FancyURLopener
from urllib.request import urlopen as uReq
# beafrom urllib.request import urlretrieve as getImg
from bs4 import BeautifulSoup as soup


class AppURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/2007127 Firefox/2.0.0.11"


opener = AppURLopener()

name = input("Enter manga name $>")
name = name.replace(" ", "-")

os.makedirs(name)
url = "http://www.mangareader.net/" + name
print(url)

client = uReq(url)
html_page = client.read()
client.close()

parsed_page = soup(html_page, "html.parser")

list_chapter = parsed_page.findAll("div", {"class": "chico_manga"})

start = input("Enter Lower Limit  :>")
if int(start) < 1:
    start = 1

stop = input("Enter Upper Limit :>")
while int(stop) > len(list_chapter):
    stop = input("(Invalid Upper Limit)Enter Upper Limit :>")

for i in range(int(start), int(stop)):
    manga_url = uReq(url + '/{i}'.format(**vars()))
    print("Downloading" + url + '/' + str(i))
    html_page = manga_url.read()
    manga_url.close()
    parsed_page = soup(html_page, "html.parser")

    chapter_size = parsed_page.find("div", {"id": "selectpage"}).text
    chapter_size = chapter_size.split()
    l = len(chapter_size)
    chapter_size = chapter_size[l - 1]
    print(chapter_size)
    os.makedirs(name + "/" + str(i))

    for j in range(1, int(chapter_size) + 1):
        manga_url = uReq(url + '/' + str(i) + '/' + str(j))
        print("Downloading Image :" + '/' + str(i) + '/' + str(j))
        html_page = manga_url.read()
        manga_url.close()
        parsed_page = soup(html_page, "html.parser")
        image = parsed_page.find("img", {"id": "img"})["src"]
        local_name = name + "/" + str(i) + "/" + str(j)
        opener.retrieve(image, local_name + ".jpg")

    print("Completed chapter : " + str(i))
