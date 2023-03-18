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
            def __init__(self,name):
                self.runs=0
                self.balls_faced=0
                self.name=name
                self.num_fours=0
                self.num_sixes=0
                self.out=False
            def print_score(self):
                if(self.balls_faced>0):
                    print(self.name+":"+str(self.runs)+" from "+str(self.balls_faced)+", "+str(self.num_fours)+" fours, "+str(self.num_sixes)+" sixes")
        def __init__(self,team):
            self.score=0
            self.name=team.name
            
            self.players=[]
            for i in range(len(team.players)):
                self.players.append(self.player(team.players[i]))
            self.striker=0
            self.non_striker=1
            self.wickets_lost=0
        def print_score(self):
            print(self.name+":"+str(self.score)+"/"+str(self.wickets_lost))
            for player in self.players:
                player.print_score()
    def __init__(self,team1,team2):
        self.team1=self.team(team1)
        self.team2=self.team(team2)
        self.over_count=0
        
    def next_over(self,team):
        self.over_count+=1
        scores=(random.choices([-2,0,1,2,3,4,6], weights=(7,46, 46, 10, 1, 12, 6), k=6))
        for i in range(6):
            team.score+=scores[i]
            if(scores[i]==4):
                team.players[team.striker].num_fours+=1
            if(scores[i]==6):
                team.players[team.striker].num_sixes+=1
            team.players[team.striker].runs+=scores[i]
            team.players[team.striker].balls_faced+=1
            if(scores[i]==-2):
                team.score+=2
                team.players[team.striker].runs+=2
                team.players[team.striker].out=True
                team.wickets_lost+=1
                if(max(team.non_striker,team.striker)<=9):
                    team.striker=max(team.non_striker,team.striker)+1
            if(scores[i]%2==1):
                temp=team.non_striker
                team.non_striker=team.striker
                team.striker=temp
            if(self.over_count>20):
                if(team.score>self.team1.score or team.score>self.team2.score):
                    return
            if(team.wickets_lost==10):
                return
        temp=team.non_striker
        team.non_striker=team.striker
        team.striker=temp
    
    def sim_match(self):
        for i in range(40):
            if(i<20):
                self.next_over(self.team1)
                if(self.team1.wickets_lost==10):
                    i=20
            else:
                self.next_over(self.team2)
                if(self.team2.score>self.team1.score or (self.team2.wickets_lost==10)):
                    i=40
        self.team1.print_score()
        self.team2.print_score()

t1=teams("Team a",["Player "+str(i)for i in range(1,12,1)])
t2=teams("Team b",["Player "+str(i)for i in range(1,12,1)])
m1=match(t1,t2)
m1.sim_match()
if(__name__=="main"):
    t1=teams("Team a",["Player "+str(i)for i in range(1,12,1)])
    t2=teams("Team b",["Player "+str(i)for i in range(1,12,1)])
    m1=match(t1,t2)
    m1.sim_match()  