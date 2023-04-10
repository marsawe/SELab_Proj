import random
from teams import Tournament
import numpy as np
#Class to store and generate relevant details for a match
class match:
    #Class to store and generate relevant match details for a team
    class team:
        #Class to store and generate relevant player details for a match
        class player:
            #Stats are separated into batting and bowling stats for clarity
            class batting:
                def __init__(self,name):
                    self.name=name
                    self.runs=0
                    self.balls_faced=0
                    self.num_fours=0
                    self.num_sixes=0
                    self.out=False
                def print_score(self):
                    if(self.balls_faced>0):
                        print(self.name+":"+str(self.runs)+" from "+str(self.balls_faced)+", "+str(self.num_fours)+" fours, "+str(self.num_sixes)+" sixes")
            class bowling:
                def __init__(self,name):
                    self.overs=0
                    self.maidens=0
                    self.runs=0
                    self.wickets=0
                    self.name=name
                def print_stats(self):
                    if(self.overs>0):
                        print((self.name)+":"+str(self.overs)+"-"+str(self.maidens)+"-"+str(self.runs)+"-"+str(self.wickets))
            def __init__(self,player):
                self.name=player.first_name+" "+player.last_name
                self.batstats=self.batting(self.name)
                self.bowlstats=self.bowling(self.name)
                
                batskills={"Batsman":(-3,-10,6,2,0,3,1),"Bowler":(2,10,-6,-2,0,-3,-1),"Wicket-Keeper":(-2,-10,6,2,0,3,1),"All-Rounder":(1,-1,-1,0,0,0,1)}
                self.batskills=batskills[player.role]
                bowlskills={"Batsman":(-3,-10,6,2,0,3,1),"Bowler":(1,10,-6,-2,0,-3,-1),"Wicket-Keeper":(-2,-10,6,2,0,3,1),"All-Rounder":(1,-1,-1,0,0,0,1)}
                self.bowlskills=bowlskills[player.role]
        def __init__(self,team):
            self.score=0
            self.name=team.name            
            self.players=[]
            for i in range(len(team.players)):
                self.players.append(self.player(team.players[i]))
            self.striker=0
            self.non_striker=1
            self.wickets_lost=0
            self.curr_bowler=10
        #Function 
        def print_score(self):
            print(self.name+":"+str(self.score)+"/"+str(self.wickets_lost))
            for player in self.players:
                player.batstats.print_score()
        def print_bowlstats(self):
            for player in self.players:
                player.bowlstats.print_stats()
    def __init__(self,team1,team2):
        self.team1=self.team(team1)
        self.team2=self.team(team2)
        self.over_count=0        
    def next_over(self,batteam,bowler):
        self.over_count+=1
        bowler.bowlstats.overs+=1
        scores=[]
        for i in range(6):
            in_weights=(8,43, 43, 10, 1, 11, 6)
            fin_weights=tuple(np.add(np.add(np.array(in_weights),np.array(batteam.players[batteam.striker].batskills)),np.array(bowler.bowlskills)))
            scores.append(random.choices([-2,0,1,2,3,4,6], weights=fin_weights, k=1)[0])
            batteam.score+=scores[i]
            bowler.bowlstats.runs+=scores[i]
            if(scores[i]==4):
                batteam.players[batteam.striker].batstats.num_fours+=1
            if(scores[i]==6):
                batteam.players[batteam.striker].batstats.num_sixes+=1
            batteam.players[batteam.striker].batstats.runs+=scores[i]
            batteam.players[batteam.striker].batstats.balls_faced+=1
            if(scores[i]==-2):
                batteam.score+=2
                bowler.bowlstats.runs+=2
                batteam.players[batteam.striker].batstats.runs+=2
                batteam.players[batteam.striker].batstats.out=True
                batteam.wickets_lost+=1
                bowler.bowlstats.wickets+=1
                if(max(batteam.non_striker,batteam.striker)<=9):
                    batteam.striker=max(batteam.non_striker,batteam.striker)+1
            if(scores[i]%2==1):
                temp=batteam.non_striker
                batteam.non_striker=batteam.striker
                batteam.striker=temp
            if(self.over_count>20):
                if(batteam.score>self.team1.score):
                    return
            if(batteam.wickets_lost>=10):
                return
        temp=batteam.non_striker
        batteam.non_striker=batteam.striker
        batteam.striker=temp
    
    def sim_match(self,team1,team2):
        
        while(self.over_count<20):
            n=random.choices([i for i in range(11)],weights=(1,1,1,1,0,2,2,4,4,4,4),k=1)[0]
            while(self.team2.players[n].bowlstats.overs==4):
                n=random.choices([i for i in range(11)],weights=(1,1,1,1,0,2,2,4,4,4,4),k=1)[0]
            self.next_over(self.team1,self.team2.players[n])
            if(self.team1.wickets_lost>=10):
                self.over_count=20
        while(self.over_count<40):
            n=random.choices([i for i in range(11)],weights=(1,1,1,1,0,4,4,8,8,8,8),k=1)[0]
            while(self.team1.players[n].bowlstats.overs==4):
                n=random.choices([i for i in range(11)],weights=(1,1,1,1,0,4,4,8,8,8,8),k=1)[0]
            self.next_over(self.team2,self.team1.players[n])
            if((self.team2.score>self.team1.score) or (self.team2.wickets_lost>=10)):
                self.over_count=40

        for i in range(11):
            team1.players[i].runs_scored+=self.team1.players[i].batstats.runs
            team1.players[i].balls_faced+=self.team1.players[i].batstats.balls_faced
            team1.players[i].wickets+=self.team1.players[i].bowlstats.wickets
            team1.players[i].overs+=self.team1.players[i].bowlstats.overs
            team1.players[i].runs_conceded+=self.team1.players[i].bowlstats.runs
            team2.players[i].runs_scored+=self.team2.players[i].batstats.runs
            team2.players[i].balls_faced+=self.team2.players[i].batstats.balls_faced
            team2.players[i].wickets+=self.team2.players[i].bowlstats.wickets
            team2.players[i].overs+=self.team2.players[i].bowlstats.overs
            team2.players[i].runs_conceded+=self.team2.players[i].bowlstats.runs
    def print_scores(self):
        self.team1.print_score()
        self.team2.print_bowlstats()
        self.team2.print_score()
        self.team1.print_bowlstats()
    
