if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd() + "/../libs/")
    import summary_structure as ss


import urllib2 as url
from lxml import etree
from StringIO import StringIO
from pygame.examples.aliens import SCORE

espn_url = "http://espn.go.com/college-football/game?gameId=400787110"

req = url.Request(espn_url)

quarter_names = {"first Quarter": 1, "second Quarter": 2, "third Quarter": 3, "fourth Quarter":4}

try:
    response = url.urlopen(req)
except URLError as e:
    print e.reason
    sys.exit()
    
html = response.read()

parser = etree.HTMLParser()

root = etree.fromstring(html, parser)

summary = root.find(".//*[@class='scoring-summary']")

for x in summary:
    if x.tag == "table":
        summary = x[0]

away_team = summary.find(".//*[@class='home-team']").text
home_team = summary.find(".//*[@class='away-team']").text

for x in summary:
    if not x.findall(".//*[@class='quarter']") == []:
        print quarter_names[x[0].text], "Quarter found"
    else:
        instance = ss.Score()
        raw_scoring_play = x
        details = raw_scoring_play.find(".//*[@class='game-details']")[0]
        instance.details[0].text
        
        
