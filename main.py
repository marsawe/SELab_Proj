from teams import Tournament
from match import match
from schedule import Schedule
import mysql.connector 


if __name__ == '__main__':
    connector=mysql.connector.connect(user='root',password='Kannan2003',host='localhost',database='cricket')
    cursor = connector.cursor()
    
    T=Tournament()
    T.load_data()
    T.generate_teams(8)
    schedule=Schedule()
    with open('tournament_team_names.txt',"r") as f:
        for team_name in f:
            l=team_name.split(",")
        for team_name in l :
            schedule.add_team(team_name)

    venues = ['M. A. Chidambaram Stadium, Chennai', 'Wankhede Stadium, Mumbai', 'Eden Gardens, Kolkata', 'Arun Jaitley Stadium, Delhi', 'M. Chinnaswamy Stadium, Bengaluru', 'Sawai Mansingh Stadium, Jaipur', 'Punjab Cricket Association Stadium, Mohali', 'Rajiv Gandhi International Cricket Stadium, Hyderabad']
    for venue in venues:
        schedule.add_venue(venue)
    schedule.generate_schedule()
    schedule.print_schedule("schedule.txt")
    #creating schedule table in database
    cursor.execute("drop table if exists schedule")
    cursor.execute("create table schedule(Match_no int(2) , date varchar(15), time varchar(10),stadium varchar(50) , venue varchar(20), team1 varchar(30), team2 varchar(30), primary key(Match_no))")
    
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
    
    
    
    
        
        
    
                
        
    
    
    
    
    
   