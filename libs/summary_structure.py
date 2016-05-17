import re

class Handler():
    def scoring_play(self, line):
        m = re.search('.* (P|p)ass .*')
        


class Score():
    def __init__(self):
        self.home_score = 0
        self.visit_score = 0
        self.yds = 0
        self.player_name = ""
        self.time = ""
        self.team = ""
        self.kicker = ""
        
    def parse_kick(self, line):
        kick_line = line[line.find('(')+1:line.find(')')]
        m = re.search('Kick|PAT failed|PAT blocked', kick_line)
        self.kicker = kick_line.replace(m.group(0), "")
        self.kick_res = kick_status[m.group(0)]

    def parse_drive(self, line):
        self.drive_plays = re.search('\d+', re.search('\d+ play(s)?', line).group(0)).group(0)
        self.drive_yards = re.search('\d+', re.search('\d+ y(ar)?ds', line).group(0)).group(0)
        self.drive_time = re.search('\d+:\d+', line)
        if not self.drive_time is None:
            self.drive_time = self.drive_time.group(0)
        else:
            self.drive_time = ""
        return self.parse_score(line)

    def parse_score(self, line):
        m = re.search('\t( \D+)?\d+( - \D+|\t)(\D+)?(\d+)', line)
        if not m == None:
            scores = re.findall('\d+', m.group(0))
            self.home_score = scores[1]
            self.visit_score = scores[0]
            self.team = self.get_scoring_team()
            global current_score
            current_score = [self.visit_score, self.home_score]
            return True
        else:
            return False
    
    def get_scoring_team(self):
        if not self.visit_score == current_score[0] and self.home_score == current_score[1]:
            return teams['Visitor']
        else:
            return teams['Home']
    def get_wiki():
        pass
    def write_wiki(self):
        with open("output.txt", 'a') as f:
            f.write(self.wiki_string)

    
class IntScore(Score):
    def __init__(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.visit_score = datas[3]
        self.home_score = datas[4]
        self.parse_kick(datas[2])
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=IntTD\n"
        self.wiki_string +="| Def={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(self.kick_res)
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
class Pass_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.qb = re.search('(f|F)rom .*\(', datas[2]).group(0).replace('from ', "").replace(' (', "")
        self.parse_kick(line)
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| DrivePlays={}\n".format(self.drive_plays)
        self.wiki_string +="| DriveLength={}\n".format(self.drive_yards)
        self.wiki_string +="| DriveTime={}\n".format(self.drive_time)
        self.wiki_string +="| Type=RecTD\n"
        self.wiki_string +="| Receiver={}\n".format(self.player_name)
        self.wiki_string +="| QB={}\n".format(self.qb)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(self.kick_res)
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
class Run_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.parse_kick(line)
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| DrivePlays={}\n".format(self.drive_plays)
        self.wiki_string +="| DriveLength={}\n".format(self.drive_yards)
        self.wiki_string +="| DriveTime={}\n".format(self.drive_time)
        self.wiki_string +="| Type=RushTD\n"
        self.wiki_string +="| Runner={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(self.kick_res)
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"



class FG_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| DrivePlays={}\n".format(self.drive_plays)
        self.wiki_string +="| DriveLength={}\n".format(self.drive_yards)
        self.wiki_string +="| DriveTime={}\n".format(self.drive_time)
        self.wiki_string +="| Type=FG\n"
        self.wiki_string +="| Kicker={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"

class Fum_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.parse_kick(line)
        if(len(datas)>2):
            self.team = self.get_scoring_team()
            self.visit_score = datas[3]
            self.home_score = datas[4]
            return True
        else:
            return False

    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=FumbleTD\n"
        self.wiki_string +="| Def={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(self.kick_res)
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"

class PR_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.parse_kick(line)
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=Other\n"
        self.wiki_string +="| Other={}{} yard punt return,".format(self.player_name, self.yds)
        if not self.kicker == "":
            self.wiki_string +=" {}".format(self.kicker)
            self.wiki_string +="kick {}\n".format(self.kick_res)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
class PAT_Conv_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.visit_score = datas[3]
        self.home_score = datas[4]
        self.team = self.get_scoring_team()
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=Other\n"
        self.wiki_string +="| Other={}\n".format(self.player_name)
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
class KR_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.player_name = re.search('\D+', datas[2]).group(0)
        self.yds = re.search('\d+',datas[2]).group(0)
        self.parse_kick(line)
        self.visit_score = datas[3]
        self.home_score = datas[4]
        self.team = self.get_scoring_team()
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=Other\n"
        self.wiki_string +="| Other={}{} yard kick return,".format(self.player_name, self.yds)
        if not self.kicker == "":
            self.wiki_string +=" {}".format(self.kicker)
            self.wiki_string +="kick {}\n".format(self.kick_res)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"

class Team_Safe_Score(Score):
    def parse_actions(self, line):
        datas = line.split('\t')
        self.time = datas[1]
        self.visit_score = datas[3]
        self.home_score = datas[4]
        self.team = self.get_scoring_team()
        
    def get_wiki(self):
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=SafetyOther\n"
        self.wiki_string +="| Info=Team Safety\n"
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        