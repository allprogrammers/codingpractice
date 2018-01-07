import urllib.request
#import urllib2
from bs4 import BeautifulSoup

youtubefile = open("youtube.txt","w")

with open("songlist.txt","r") as f:
    for line in f:
        textToSearch = line
        query=urllib.request.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,"html5lib")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            youtubefile.write('https://www.youtube.com' + vid['href']+'\n')
            break
