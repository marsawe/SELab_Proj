import random
class teams:
    def __init__(self,name,players):
        self.name=name
       
        self.player1=players[0]
        self.player2=players[1]
class match:
    class team:
        class player:
            def __init__(self,name):
                self.runs=0
                self.balls_faced=0
                self.name=name
                self.num_fours=0
                self.num_sixes=0
        def __init__(self,team):
            self.score=0
            self.name=team.name
            
            self.player1=self.player(team.player1)
            self.player2=self.player(team.player2)
            self.curr_bat=self.player1
    def __init__(self,team1,team2):
        self.team1=self.team(team1)
        self.team2=self.team(team2)
        self.over_count=0
        
    def next_over(self,team):
        self.over_count+=1
        scores=(random.choices([0,1,2,3,4,6], weights=(46, 46, 10, 1, 12, 6), k=6))
        for i in range(6):
            team.score+=scores[i]
            if(scores[i]==4):
                team.curr_bat.num_fours+=1
            if(scores[i]==6):
                team.curr_bat.num_sixes+=1
            team.curr_bat.runs+=scores[i]
            team.curr_bat.balls_faced+=1
            if(team.curr_bat==team.player1):
                if(scores[i]%2==1):
                    team.curr_bat= team.player2
            else:
                if(scores[i]%2==1):
                    team.curr_bat= team.player1
            if(self.over_count>20):
                if(team.score>self.team1.score or team.score>self.team2.score):
                    return
        if(team.curr_bat==team.player1):
            team.curr_bat=team.player2
        else:
            team.curr_bat=team.player1
        
    def sim_match(self):
        for i in range(40):
            if(i<20):
                self.next_over(self.team1)
            else:
                self.next_over(self.team2)
        print(self.team1.name+":"+str(self.team1.score))
        print(self.team2.name+":"+str(self.team2.score))
        print(self.team1.player1.name+":"+str(self.team1.player1.runs)+" from "+str(self.team1.player1.balls_faced)+", "+str(self.team1.player1.num_fours)+"fours, "+str(self.team1.player1.num_sixes)+"sixes,")
        print(self.team1.player2.name+":"+str(self.team1.player2.runs)+" from "+str(self.team1.player2.balls_faced)+", "+str(self.team1.player2.num_fours)+"fours, "+str(self.team1.player2.num_sixes)+"sixes,")
        print(self.team2.player1.name+":"+str(self.team2.player1.runs)+" from "+str(self.team2.player1.balls_faced)+", "+str(self.team2.player1.num_fours)+"fours, "+str(self.team2.player1.num_sixes)+"sixes,")
        print(self.team2.player2.name+":"+str(self.team2.player2.runs)+" from "+str(self.team2.player2.balls_faced)+", "+str(self.team2.player2.num_fours)+"fours, "+str(self.team2.player2.num_sixes)+"sixes,")

t1=teams("Team a",["Player P","Player Q"])
t2=teams("Team b",["Player R","Player S"])
m1=match(t1,t2)
m1.sim_match()

        