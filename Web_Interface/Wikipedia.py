kick_status = {'Kick':'good', 'PAT failed':'no good', 'PAT blocked':'no good (blocked)'}  

def generate_wikipedia(input_class):
    wiki_string = ""
    class_name = input_class.__class__.__name__
    
    if class_name == "Team_Safe_Score":
        wiki_string = "{{AmFootballScoreSummaryEntry\n"
        wiki_string +="| Quarter={}\n".format(input_class.quarter)
        wiki_string +="| Time={}\n".format(input_class.time)
        wiki_string +="| Team={}\n".format(input_class.team)
        wiki_string +="| Type=SafetyOther\n"
        wiki_string +="| Info=Team Safety\n"
        wiki_string +="| Visitor={}\n".format(input_class.visit_score)
        wiki_string +="| Home={}\n".format(input_class.home_score)
        wiki_string +="}}\n"
        
    if class_name == "KR_Score":
        wiki_string = "{{AmFootballScoreSummaryEntry\n"
        wiki_string +="| Quarter={}\n".format(input_class.quarter)
        wiki_string +="| Time={}\n".format(input_class.time)
        wiki_string +="| Team={}\n".format(input_class.team)
        wiki_string +="| Type=Other\n"
        wiki_string +="| Other={}{} yard kick return,".format(input_class.player_name, input_class.yds)
        if not input_class.kicker == "":
            wiki_string +=" {}".format(input_class.kicker)
            wiki_string +="kick {}\n".format(kick_status[input_class.kick_res])
        else:
            wiki_string +="| 2pt type={}\n".format("")
            wiki_string +="| 2pt result={}\n".format("")
        wiki_string +="| Visitor={}\n".format(input_class.visit_score)
        wiki_string +="| Home={}\n".format(input_class.home_score)
        wiki_string +="}}\n"
        
    if class_name == "PAT_Conv_Score":
        wiki_string = "{{AmFootballScoreSummaryEntry\n"
        wiki_string +="| Quarter={}\n".format(input_class.quarter)
        wiki_string +="| Time={}\n".format(input_class.time)
        wiki_string +="| Team={}\n".format(input_class.team)
        wiki_string +="| Type=Other\n"
        wiki_string +="| Other={}\n".format(input_class.player_name)
        wiki_string +="| Visitor={}\n".format(input_class.visit_score)
        wiki_string +="| Home={}\n".format(input_class.home_score)
        wiki_string +="}}\n"
        
    if class_name == "PR_Score":
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=Other\n"
        self.wiki_string +="| Other={}{} yard punt return,".format(self.player_name, self.yds)
        if not self.kicker == "":
            self.wiki_string +=" {}".format(self.kicker)
            self.wiki_string +="kick {}\n".format(kick_status[input_class.kick_res])
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
    if class_name == "Fum_Score":
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=FumbleTD\n"
        self.wiki_string +="| Def={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(kick_status[input_class.kick_res])
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
    if class_name == "FG_Score":
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
        
    if class_name == "Run_Score":
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
            self.wiki_string +="| kickresult={}\n".format(kick_status[input_class.kick_res])
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
    if class_name == "Pass_Score":
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
            self.wiki_string +="| kickresult={}\n".format(kick_status[input_class.kick_res])
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"
        
    if class_name == "IntScore":
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=IntTD\n"
        self.wiki_string +="| Def={}\n".format(self.player_name)
        self.wiki_string +="| yards={}\n".format(self.yds)
        if not self.kicker == "":
            self.wiki_string +="| kickresult={}\n".format(kick_status[input_class.kick_res])
            self.wiki_string +="| Kicker={}\n".format(self.kicker)
        else:
            self.wiki_string +="| 2pt type={}\n".format("")
            self.wiki_string +="| 2pt result={}\n".format("")
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"