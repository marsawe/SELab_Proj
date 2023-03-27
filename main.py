from teams import Tournament
from match import match
from schedule import Schedule
import mysql.connector 


def simulate_match(id):
    cursor=connector.cursor()
    cursor.execute("select team1 , team2 from schedule where Match_no={}".format(id))
    teams=cursor.fetchone()
    team1=teams[0]
    team2=teams[1]
    
    for team in T.teams :
        if team.name==team1:
            team1=team
        if team.name==team2:
            team2=team
    
    m=match(team1,team2)
    m.sim_match(team1,team2)
    # m.print_scores()
    
    cursor.execute("drop table if exists match_{}_bat1".format(id))
    cursor.execute("Create table match_{}_bat1 (batting_position int(2) PRIMARY KEY AUTO_INCREMENT,batter varchar(30),runs int(3),balls int(3),fours int(2),sixes int(2),strike_rate float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bowl2".format(id))
    cursor.execute("Create table match_{}_bowl2 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs int(2),runs int(3),wickets int(2),economy float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bat2".format(id))
    cursor.execute("Create table match_{}_bat2 (batting_position int(2) AUTO_INCREMENT PRIMARY KEY,batter varchar(30),runs int(3),balls int(3),fours int(2),sixes int(2),strike_rate float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bowl1".format(id))
    cursor.execute("Create table match_{}_bowl1 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs int(2),runs int(3),wickets int(2),economy float)".format(id))
    

    # team 1 batting stat
    for player in m.team1.players :
        if(player.batstats.balls_faced>0):
            strike_rate=round(player.batstats.runs/player.batstats.balls_faced*100,2)
        else :
            strike_rate=0
        cursor.execute("insert into match_{}_bat1(batter,runs,balls,fours,sixes,strike_rate) values(\'{}\',{},{},{},{},{})".format(id,player.name,player.batstats.runs,player.batstats.balls_faced,player.batstats.num_fours,player.batstats.num_sixes,strike_rate))
        connector.commit()
        if(player.bowlstats.overs>0):
            cursor.execute("insert into match_{}_bowl1(bowler,overs,runs,wickets,economy) values(\'{}\',{},{},{},{})".format(id,player.name,player.bowlstats.overs,player.bowlstats.runs,player.bowlstats.wickets,player.bowlstats.runs/player.bowlstats.overs))
            connector.commit()
    
    #team 2 batting stat
    for player in m.team2.players :
        if(player.batstats.balls_faced>0):
            strike_rate=round(player.batstats.runs/player.batstats.balls_faced*100,2)
        else :
            strike_rate=0
        cursor.execute("insert into match_{}_bat2(batter,runs,balls,fours,sixes,strike_rate) values(\'{}\',{},{},{},{},{})".format(id,player.name,player.batstats.runs,player.batstats.balls_faced,player.batstats.num_fours,player.batstats.num_sixes,strike_rate))
        connector.commit()
        if(player.bowlstats.overs>0):
            cursor.execute("insert into match_{}_bowl2(bowler,overs,runs,wickets,economy) values(\'{}\',{},{},{},{})".format(id,player.name,player.bowlstats.overs,player.bowlstats.runs,player.bowlstats.wickets,player.bowlstats.runs/player.bowlstats.overs))
            connector.commit()
            
    
    #updating points table
    if(m.team1.score > m.team2.score) : 
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team1.name))
        team1_matches=cursor.fetchone()[0]
        if(len(team1_matches)==5):
            team1_matches=team1_matches[0:4]
        team1_matches="W"+team1_matches
        cursor.execute("update points_table set played=played+1 , won=won+1 , points=points+2 , last_5_matches=\'{}\' where team=\'{}\'".format(team1_matches,team1.name))
        connector.commit()
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team2.name))
        team2_matches=cursor.fetchone()[0]
        if(len(team2_matches)==5):
            team2_matches=team2_matches[0:4]
        team2_matches="L"+team2_matches
        cursor.execute("update points_table set played=played+1 , lost=lost+1 ,last_5_matches=\'{}\' where team=\'{}\'".format(team2_matches,team2.name))
        connector.commit()
    elif(m.team1.score < m.team2.score) :
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team2.name))
        team2_matches=cursor.fetchone()[0]
        if(len(team2_matches)==5):
            team2_matches=team2_matches[0:4]
        team2_matches="W"+team2_matches
        cursor.execute("update points_table set played=played+1 , won=won+1 , points=points+2 , last_5_matches=\'{}\' where team=\'{}\'".format(team2_matches,team2.name))
        connector.commit()
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team1.name))
        team1_matches=cursor.fetchone()[0]
        if (len(team1_matches)==5):
            team1_matches=team1_matches[0:4]
        team1_matches="L"+team1_matches
        cursor.execute("update points_table set played=played+1 , lost=lost+1 ,last_5_matches=\'{}\' where team=\'{}\'".format(team1_matches,team1.name))
        connector.commit()
    else :
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team1.name))
        team1_matches=cursor.fetchone()[0]
        if (len(team1_matches)==5):
            team1_matches=team1_matches[0:4]
        team1_matches="D"+team1_matches
        cursor.execute("update points_table set played=played+1 , drawn=drawn+1 , points=points+1 , last_5_matches=\'{}\' where team=\'{}\'".format(team1_matches,team1.name))
        connector.commit()
        cursor.execute("select last_5_matches from points_table where team=\'{}\'".format(team2.name))
        team2_matches=cursor.fetchone()[0]
        if (len(team2_matches)==5):
            team2_matches=team2_matches[0:4]
        team2_matches="D"+team2_matches
        cursor.execute("update points_table set played=played+1 , drawn=drawn+1 , points=points+1 , last_5_matches=\'{}\' where team=\'{}\'".format(team2_matches,team2.name))
        connector.commit()
    
def show_points_table() :
    cursor=connector.cursor()
    cursor.execute("select * from points_table order by points desc")
    table=cursor.fetchall()
    cursor.close()
    return table
    

if __name__ == '__main__':
    passcode=input("Enter password for mysql : ")
    connector=mysql.connector.connect(user='root',password=passcode,host='localhost',database='cricket')
    cursor = connector.cursor()
    cursor.execute("create database if not exists cricket")
    cursor.execute("use cricket")
    
    T=Tournament()
    T.load_data()
    T.generate_teams(8)
    
    
    
    cursor.execute("drop table if exists match_id")
    cursor.execute("create table match_id(match_no int(2) primary key)")
    cursor.execute("insert into match_id values(0)")
    while(True) :
        print("Enter 1 to generate schedule\nEnter 2 to simulate a match\nEnter 3 to show points table\nEnter 4 to see the schedule\nEnter 5 to see scorecard of a particular match\nEnter 6 to exit")
        choice=int(input())
        if choice==1 :
            #generating Schedule and pushing it to sql database
            schedule=Schedule()
            
            #creating schedule table in database
            cursor.execute("drop table if exists schedule")
            cursor.execute("create table schedule(Match_no int(2) , date varchar(15), time varchar(10),stadium varchar(50) , venue varchar(20), team1 varchar(30), team2 varchar(30), primary key(Match_no))")
            #creating points table in database
            cursor.execute("drop table if exists points_table")
            cursor.execute("create table points_table(team varchar(30),played int(2),won int(2),lost int(2),drawn int(2),points int(2),last_5_matches varchar(5))")
            
            
            with open('tournament_team_names.txt',"r") as f:
                for team_name in f:
                    l=team_name.split(",")
                for team_name in l :
                    schedule.add_team(team_name)
                    cursor.execute("insert into points_table(team,played,won,lost,drawn,points,last_5_matches) values(\'{}\',0,0,0,0,0,\'\')".format(team_name))

            venues = ['M. A. Chidambaram Stadium, Chennai', 'Wankhede Stadium, Mumbai', 'Eden Gardens, Kolkata', 'Arun Jaitley Stadium, Delhi', 'M. Chinnaswamy Stadium, Bengaluru', 'Sawai Mansingh Stadium, Jaipur', 'Punjab Cricket Association Stadium, Mohali', 'Rajiv Gandhi International Cricket Stadium, Hyderabad']
            for venue in venues:
                schedule.add_venue(venue)
            schedule.generate_schedule()
            schedule.print_schedule("schedule.txt")
            
            
            with open("schedule.txt","r") as f :
                i=1
                for x in f : 
                    l=x.split(",")
                    
                    date=l[0].strip()
                    time=l[1].strip()
                    stadium=l[2].strip()
                    venue=l[3].strip()
                    team1=l[4].strip()
                    team2=l[5].strip("\n")
                    sql="INSERT INTO schedule VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(i,date,time,stadium,venue,team1,team2)
                    cursor.execute(sql)
                    connector.commit()
                    i+=1
            cursor.close()
            #End of creating a schedule table in database
            
        elif choice==2 :
            cursor=connector.cursor()
            n=int(input("Enter the the number of matches you want to simulate : "))
            cursor.execute("select max(match_no) from match_id")
            match_id=cursor.fetchone()[0]
            cursor.execute("Update match_id set match_no=match_no+{}".format(n))
            connector.commit()
            for match_num in range(match_id+1,match_id+n+1) :
                simulate_match(match_num)
            cursor.close()
        elif choice==3 :
            points_table=show_points_table()
            for row in points_table:
                print(row)
        elif choice==4 :
            cursor=connector.cursor()
            cursor.execute("select * from schedule")
            schedule=cursor.fetchall()
            for row in schedule :
                print(row)
            cursor.close()
        elif choice==5 :
            cursor=connector.cursor()
            match_num=int(input("Enter the match number : "))
            cursor.execute("select SUM(runs) from match_{}_bat1".format(match_num))
            score=cursor.fetchone()[0]
            cursor.execute("select SUM(wickets) from match_{}_bowl2".format(match_num))
            wickets=cursor.fetchone()[0]
            cursor.execute("Select team1,team2 from schedule where match_no={}".format(match_num))
            team1,team2=cursor.fetchone()
            print("Scorecard of match {} between {} and {}".format(match_num,team1,team2))
            print(team1," : ",score,"/",wickets)
            print("Batting : ")
            cursor.execute("select * from match_{}_bat1".format(match_num))
            bat1=cursor.fetchall()
            for row in bat1 :
                print(row)
            print("Bowling : ")
            cursor.execute("select * from match_{}_bowl2".format(match_num))
            bowl2=cursor.fetchall()
            for row in bowl2 :
                print(row)
            print("----------------------")
            cursor.execute("select SUM(runs) from match_{}_bat2".format(match_num))
            score=cursor.fetchone()[0]
            cursor.execute("select SUM(wickets) from match_{}_bowl1".format(match_num))
            wickets=cursor.fetchone()[0]
            print(team2," : ",score,"/",wickets)
            print("Batting : ")
            cursor.execute("select * from match_{}_bat2".format(match_num))
            bat2=cursor.fetchall()
            for row in bat2 :
                print(row)
            print("Bowling : ")
            cursor.execute("select * from match_{}_bowl1".format(match_num))
            bowl1=cursor.fetchall()
            for row in bowl1 :
                print(row)
            cursor.close()
        elif choice==6 :
            exit()
