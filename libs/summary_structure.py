import re
           

class Score():
    def __init__(self):
        self.home_score = 0
        self.visit_score = 0
        self.yds = 0
        self.player_name = ""
        self.time = ""
        self.team = ""
        self.kicker = ""
        self.quarter = 0
    
    def parse_two_point(self, line):
        two_point_line = re.search("\(\D+\)", line).group(0).replace("(", "").replace(")", "")
        self.two_point_play = None

    def parse_kick(self, line):
        kick_line = line[line.find('(')+1:line.find(')')]
        m = re.search('Kick|PAT failed|PAT blocked', kick_line)
        if m == None:
            self.parse_two_point(line)
            return
        self.kicker = kick_line.replace(m.group(0), "")
        self.kick_res = m.group(0)

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



class Int_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)

    def __repr__(self):
        return "{} Int Return Q{} {} {} {} yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)    
    
        
class Pass_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.qb = re.search('(f|F)rom .*\(', line).group(0).replace('from ', "").replace(' (', "")
        self.parse_kick(line)
        
    def __repr__(self):
        return "{} TD Q{} {} {} from {} {} yds".format(self.team, self.quarter, self.time, self.player_name, self.qb, self.yds)
               
class Run_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)
    def __repr__(self):
        return "{} TD Q{} {} {} {} yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)

class FG_Score(Score):
    def __init__(self, line):
        Score.__init__(self)
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))

    def __repr__(self):
        return "{} FG Q{} {} {} {} yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)
    
class Fum_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)
        
    def __repr__(self):
        return "{} Fumble Return Q{} {} {} {} yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)

class PR_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)
    
    def __repr__(self):
        return "{} Punt Return Q{} {} {} {}yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)
    
class PAT_Conv_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+', line).group(0))
    def __repr__(self):
        return "{} PAT Conversion Q{} {} {} {}yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)

class KR_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)
    def __repr__(self):
        return "{} Kickoff Return Q{} {} {} {}yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)

class Team_Safe_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
    def __repr__(self):
        return "{} Team Safety {}".format(self.team, self.time)
        
class Punt_Block_Score(Score):
    def __init__(self, line):
        self.time = re.search('\d+:\d+', line).group(0)
        self.player_name = re.search('\D+', line).group(0)
        self.yds = int(re.search('\d+',line).group(0))
        self.parse_kick(line)
    def __repr__(self):
        return "{} Punt Block Q{} {} {} {}yds".format(self.team, self.quarter, self.time, self.player_name, self.yds)