#Read abreviations.json
import json
import re

team_abrev = dict()

#Read abreviations.json
with open('abreviations.json') as data_file:
    team_abrev = json.load(data_file)

def update_abrev_file():
    f = open('abreviations.json', 'w')
    f.write(json.dumps(team_abrev))
    f.close()
    
quarter = 0
current_score = [0,0]#Visitor, Home
teams = {'Visitor':"", 'Home':""} #Visitor, Home

quarters_names = {'FIRST QUARTER':1, 'SECOND QUARTER':2,'THIRD QUARTER':3, 'FOURTH QUARTER':4, 'OVERTIME':'OT'}
kick_status = {'Kick':'good', 'PAT failed':'no good', 'PAT blocked':'no good (blocked)'}

parsed = []

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
        
def read_input():
    f = open('input.txt','r')
    data = f.read()
    f.close()
    lines = data.split('\r')
    lines = data.split('\n')
    for x in range(len(lines)):
    	lines[x] = lines[x].replace("\n", "")
    	lines[x] = lines[x].replace("\r", "")
    return lines

def print_header(visitor, home):
    open('output.txt', 'w').close()
    with open("output.txt", 'a') as f:
            f.write('{')
            f.write('{{AmFootballScoreSummaryStart|VisitorName={}|HomeName={}}}'.format(visitor, home))
            f.write('}\n')
            f.close()

def print_footer():
    with open("output.txt", 'a') as f:
            f.write('{')
            f.write('{{AmFootballScoreSummaryEnd|Visitor={}|Home={}}}'.format(current_score[0], current_score[1]))
            f.write('}\n')
            f.close()
            
def is_new_stat(line):
    token = line.split('\t')
    if 'FG' is token:
        return True
    elif 'TD' is token:
        return True
    elif '2P' is token:
        return True
    elif 'SF' is token:
        return True
    else:
        return False
    
    
def parse(lines):
    x = 0
    #Get Home and Visiting Teams
    try:
        teams['Visitor'] = team_abrev[lines[x].split('\t')[1]]
    except KeyError:
        user_input = input("{} not found. Please enter the non abreviatied name: ".format(lines[x].split('\t')[1]))
        team_abrev[lines[x].split('\t')[1]] = user_input
        teams['Visitor'] = team_abrev[lines[x].split('\t')[1]]
    try:
        teams['Home'] = team_abrev[lines[x].split('\t')[2]]
    except KeyError:
        user_input = input("{} not found. Please enter the non abreviatied name: ".format(lines[x].split('\t')[2]))
        team_abrev[lines[x].split('\t')[2]] = user_input
        teams['Visitor'] = team_abrev[lines[x].split('\t')[2]]
    print_header(teams['Visitor'], teams['Home'])
    update_abrev_file()
    cur_home_score = 0
    cur_away_score = 0
    #Main Parser
    while(x<len(lines)):
        if lines[x].split('\t')[0] in quarters_names.keys():
            global quarter
            quarter = quarters_names[lines[x].split('\t')[0]]
            x += 1
                

        elif 'interception' in lines[x].lower():
            int_score = IntScore(lines[x])
            int_score.get_wiki()
            int_score.write_wiki()
            x += 1
        

        elif 'pass' in lines[x].lower():
            pass_score = Pass_Score()
            pass_score.parse_actions(lines[x])
            x+=1
            if not is_new_stat(lines[x]):
                pass_score.parse_drive(lines[x])
                x+=1
                if not is_new_stat(lines[x]):
                    pass_score.parse_score(lines[x])
                    x+=1
            pass_score.get_wiki()
            pass_score.write_wiki()
            

        elif 'run' in lines[x].lower():
            run_score = Run_Score()
            run_score.parse_actions(lines[x])
            x+=1
            if not is_new_stat(lines[x]):
                run_score.parse_drive(lines[x])
                x+=1
                if not is_new_stat(lines[x]):
                    run_score.parse_score(lines[x])
                    x+=1
            run_score.get_wiki()
            run_score.write_wiki()

        elif 'field goal' in lines[x].lower() or 'fg' in lines[x].lower():
            fg_score = FG_Score()
            fg_score.parse_actions(lines[x])
            x+=1
            if not is_new_stat(lines[x]):
                fg_score.parse_drive(lines[x])
                x+=1
                if not is_new_stat(lines[x]):
                    fg_score.parse_score(lines[x])
                    x+=1
            fg_score.get_wiki()
            fg_score.write_wiki()

        elif 'fumble return' in lines[x].lower():
            fum_score = Fum_Score()
            fum_score.parse_actions(lines[x])
            x+=1
            if not is_new_stat(lines[x]):
                fum_score.parse_drive(lines[x])
                x+=1
                if not is_new_stat(lines[x]):
                    fum_score.parse_score(lines[x])
                    x+=1
            fum_score.get_wiki()
            fum_score.write_wiki()

        elif 'punt return' in lines[x].lower():
            pr_score = PR_Score()
            pr_score.parse_actions(lines[x])
            x+=1
            if not is_new_stat(lines[x]):
                pr_score.parse_drive(lines[x])
                x+=1
                if not is_new_stat(lines[x]):
                    pr_score.parse_score(lines[x])
                    x+=1
            pr_score.get_wiki()
            pr_score.write_wiki()
            x+=1

        elif 'Defensive PAT Conversion' in lines[x]:
            pat = PAT_Conv_Score()
            pat.parse_actions(lines[x])
            pat.get_wiki()
            pat.write_wiki()
            x+=1

        elif 'Team Safety' in lines[x]:
            safe = Team_Safe_Score()
            safe.parse_actions(lines[x])
            safe.get_wiki()
            safe.write_wiki()
            x+=1
            
        elif 'kickoff return' in lines[x].lower():
            pr_score = KR_Score()
            pr_score.parse_actions(lines[x])
            if not is_new_stat(lines[x]):
                pr_score.parse_score(lines[x])
                x+=1
            pr_score.get_wiki()
            pr_score.write_wiki()
            x+=1
            
        else:
            print "No Parser exists for this line: {}".format(lines[x])
            x+=1
    print_footer()
    
parse(read_input())
