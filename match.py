import random
class teams:
    def __init__(self,name,players):
        self.name=name
        self.players=[]
        for i in range(len(players)):
            self.players.append(players[i])
class match:
    class team:
        class player:
            class batting:
                def __init__(self,name):
                    self.runs=0
                    self.balls_faced=0
                    self.num_fours=0
                    self.num_sixes=0
                    self.name=name
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
            def __init__(self,name):
                self.batstats=self.batting(name)
                self.bowlstats=self.bowling(name)
                self.name=name
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
        scores=(random.choices([-2,0,1,2,3,4,6], weights=(7,46, 46, 10, 1, 12, 6), k=6))
        for i in range(6):
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
    
    def sim_match(self):
        for i in range(40):
            if(i<20):
                self.next_over(self.team1,self.team2.players[random.randint(0, 10)])
                if(self.team1.wickets_lost>=10):
                    i=20
            else:
                self.next_over(self.team2,self.team1.players[random.randint(0, 10)])
                if((self.team2.score>self.team1.score) or (self.team2.wickets_lost>=10)):
                    i=40
        self.team1.print_score()
        self.team2.print_bowlstats()
        self.team2.print_score()
        self.team1.print_bowlstats()
t1=teams("Team a",["Player "+str(i)for i in range(1,12,1)])
t2=teams("Team b",["Player "+str(i)for i in range(1,12,1)])
m1=match(t1,t2)
m1.sim_match()
if(__name__=="main"):
    t1=teams("Team a",["Player "+str(i)for i in range(1,12,1)])
    t2=teams("Team b",["Player "+str(i)for i in range(1,12,1)])
    m1=match(t1,t2)
    m1.sim_match()  