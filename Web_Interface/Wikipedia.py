def generate_wikipedia(input_class):
    
    if input_class.__name__ == "Team_Safe_Score":
        self.wiki_string = "{{AmFootballScoreSummaryEntry\n"
        self.wiki_string +="| Quarter={}\n".format(quarter)
        self.wiki_string +="| Time={}\n".format(self.time)
        self.wiki_string +="| Team={}\n".format(self.team)
        self.wiki_string +="| Type=SafetyOther\n"
        self.wiki_string +="| Info=Team Safety\n"
        self.wiki_string +="| Visitor={}\n".format(self.visit_score)
        self.wiki_string +="| Home={}\n".format(self.home_score)
        self.wiki_string +="}}\n"