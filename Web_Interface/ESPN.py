if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd() + "/../libs/")
    import summary_structure as ss


import urllib2 as url
from lxml import etree
from StringIO import StringIO
import re
import time

team_ids = dict()
team_names = dict()

schedule = []

def get_webpage(espn_url):
    req = url.Request(espn_url)
    try:
        response = url.urlopen(req)
    except URLError as e:
        print e.reason
        sys.exit()
    html = response.read()
    parser = etree.HTMLParser()
    root = etree.fromstring(html, parser)
    return root

def get_team_ids():
    global team_ids
    espn_url = "http://espn.go.com/college-football/teams"
    thing = get_webpage(espn_url)
    conferences = thing.findall(".//*[@class='medium-logos']")
    for x in conferences:
        for y in x:
            id_num = (re.search("\d+", y[0][0].attrib['href'])).group(0)
            team_ids[int(id_num)] = y[0][0].text
            team_names[y[0][0].text] = int(id_num)

##TODO: Split this in to two functions            
def get_schedule(team_id, year = time.strftime("%Y")):
    espn_url = "http://espn.go.com/college-football/team/schedule/_/id/{}/year/{}/".format(team_id, year)
    thing = get_webpage(espn_url).find(".//*[@id='showschedule']")[0][0]
    schedule = thing.findall('tr')[2:]
    schedule_times = []
    for x in schedule:
        if len(x)>1:
            date_string = "%a, %b %d %Y"
            date = x[0].text.replace("Sept", "Sep") + " " + str(year)
    
            result_time = x[2].text
            if not result_time == None:
                game_time = re.search("\d+:\d+ (AM|PM)", result_time)
                date += " " + game_time.group(0)
                date_string += " %I:%M %p"
            game_id = x.find(".//*[@class='score']")
            
            if not game_id == None:
                schedule_times.append(re.search("\d+", game_id[0].attrib['href']).group(0))
            elif x[3].text == "TBD":
                schedule_times.append(x)
            else:
                schedule_times.append(time.strptime(date, date_string))
        
    return schedule_times

def handle_game_summary(game_id):
    if type(game_id) == time.struct_time:
        return
    espn_url = "http://espn.go.com/college-football/game?gameId={}".format(game_id)
    quarter_names = {"first Quarter": 1, "second Quarter": 2, "third Quarter": 3, "fourth Quarter":4, "Overtime": "OT"}
    
    summary = get_webpage(espn_url).find(".//*[@class='scoring-summary']")

    if summary == None:
        summary = get_webpage(espn_url).find(".//*[@class='scoring-summary has-highlights']")
    for x in summary:
        if x.tag == "table":
            summary = x[0]
    
    away_team = summary.find(".//*[@class='home-team']").text
    home_team = summary.find(".//*[@class='away-team']").text
    
    quarter = 0
    
    for x in summary:
        if not x.findall(".//*[@class='quarter']") == []:
            quarter = quarter_names[x[0].text]
        else:
            raw_scoring_play = x
            details = raw_scoring_play.find(".//*[@class='game-details']")[0]
            dataline = details.find(".//*[@class='headline']").text + " " 
            time_stamp = details.find(".//*[@class='time-stamp']").text
            if not time_stamp == None:
                dataline += time_stamp
            thing = parse_summary_current(details.find(".//*[@class='score-type']").text, dataline)
            thing.quarter = quarter
            scoring_team_id =  int(re.search('\d+.png', 
                               raw_scoring_play.find(".//*[@class='logo']")[0].attrib['src']).group(0).replace(".png", ""))
            thing.team = team_ids[scoring_team_id]
            print thing

def parse_summary_current(scoring_type, scoring_play):
    if not re.search("Field Goal", scoring_play) == None:
        return ss.FG_Score(scoring_play)
    elif not re.search("pass", scoring_play) == None:
        return ss.Pass_Score(scoring_play)
    elif not re.search("Run", scoring_play) == None:
        return ss.Run_Score(scoring_play)
    elif not re.search("Punt Return", scoring_play) == None:
        return ss.PR_Score(scoring_play)
    elif not re.search("Fumble Return", scoring_play) == None:
        return ss.Fum_Score(scoring_play)
    elif not re.search("Kickoff Return", scoring_play) == None:
        return ss.KR_Score(scoring_play)
    elif not re.search("Interception Return", scoring_play) == None:
        return ss.Int_Score(scoring_play)
    elif not re.search("Return of Blocked Punt", scoring_play) == None:
        return ss.Punt_Block_Score(scoring_play)
    elif scoring_type == "SF":
        return ss.Team_Safe_Score(scoring_play)
    elif scoring_type == "D2P":
        return ss.PAT_Conv_Score(scoring_play)
    else:
        return ss.Score()
    
get_team_ids()
sch = get_schedule(team_names["Utah State"], 2014)

print sch[0]

for x in sch:
    print x
    handle_game_summary(x)

