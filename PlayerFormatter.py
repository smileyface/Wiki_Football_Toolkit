import sys


def readFile():
    f = open("Players.txt")
    content = f.readlines()
    f.close()
    return content

class Player():
    first_name = ""
    last_name = ""
    pos = ""
    num = ""
    clas = ""
    rs = ''
    def __init__(self, first_name, last_name, pos, num, clas,rs):
        self.first_name = first_name
        self.last_name = last_name
        self.pos = pos
        self.num = num
        self.clas = clas
        self.rs = rs
        
    def __str__(self):
        print "{} {} {} {} #{}".format(self.clas, self.pos, self.first_name, self.last_name, self.num)
        
    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name) 
        
    
positions_long = {"Wide Receiver/Kick Returner" : "WR", 
                  "Cornerback" : "CB", 
                  "Quarterback" : "QB",
                  "Safety" : "S",
                  "Wide Receiver" : "WR",
                  "Defensive End/Linebacker" : "LB",
                  "Running Back" : "RB",
                  "Linebacker" : "LB",
                  "Placekicker" : "PK",
                  "Tight End" : "TE",
                  "Running Back/Wide Receiver" : "RB",
                  "Cornerback/Safety" : "S",
                  "Punter" : "P",
                  "Defensive End" : "DE",
                  "Offensive Line" : "OL",
                  "Defensive Line" : "DL",
                  "Offensive Center" : "C",
                  "Offensive Guard" : "G",
                  "Long Snapper" : "LS",
                  }
                  
positions_side = {"WR" : "Offense",
                  "QB" : "Offense",
                  "RB" : "Offense",
                  "FB" : "Offense",
                  "TE" : "Offense",
                  "OL" : "Offense",
                  "OT" : "Offense",
                  "C" : "Offense",
                  "OC" : "Offense", 
                  "G" : "Offense",
                  "CB" : "Defense",
                  "S" : "Defense",
                  "SS" : "Defense",
                  "FS" : "Defense",
                  "LB" : "Defense",
                  "DE" : "Defense",
                  "DL" : "Defense",
                  "NT" : "Defense",
                  "NG" : "Defense",
                  "PK" : "Special",
                  "K" : "Special",
                  "P" : "Special",
                  "P/K" : "Special",
                  "LS" : "Special" }
def formatPlayer(player):
    output = []
    for x in range(len(player)):
        rs = ''
        if(player[x][1]=='\n'):
            x+=3
        formatted = player[x].split('\t')
        name = formatted[1].split(' ')
        if(len(formatted[4])>3):
            formatted[4] = positions_long[formatted[4]]
        if(len(name)>2):
     		name[1] = name[1] + " " + name[2]
        pos = ''
        if 'RS' in formatted[5]:
            clas = formatted[5][-2:]
            rs = 'y'
        else:
            clas = formatted[5]
     	output.append(Player(name[0], name[1], formatted[4], formatted[0], clas, rs))
        #output += ["{{American football roster/Player | pos = %s || num = %s || first = %s || last = %s || class = %s }}\n" %(formatted[4], formatted[0], name[0], name[1], formatted[5])]
    return output
    
def print_formatted(player):
    f = open("Result.txt", 'w')
    f.write("|offensive_players=\n")
    for x in player:
        if positions_side[x.pos] == "Offense":
            f.write("{{American football roster/Player | pos = %s || num = %s || first = %s || last = %s || class = %s || rs = %s}}\n" %(x.pos, x.num, x.first_name, x.last_name, x.clas, x.rs))
    f.write("|defensive_players=\n")
    for x in player:
        if positions_side[x.pos] == "Defense":
            f.write("{{American football roster/Player | pos = %s || num = %s || first = %s || last = %s || class = %s || rs = %s}}\n" %(x.pos, x.num, x.first_name, x.last_name, x.clas, x.rs))
    f.write("|special_teams_players=\n")
    for x in player:
        if positions_side[x.pos] == "Special":
            f.write("{{American football roster/Player | pos = %s || num = %s || first = %s || last = %s || class = %s || rs = %s}}\n" %(x.pos, x.num, x.first_name, x.last_name, x.clas, x.rs))

       
print_formatted(formatPlayer(readFile()))
