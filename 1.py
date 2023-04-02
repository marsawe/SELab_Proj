from tkinter import *
from teams import Tournament
from match import match
from schedule import Schedule
from functools import partial
import mysql.connector

def validateLogin(username, passcode):
    connector=mysql.connector.connect(user=username.get(),password=passcode.get(),host='localhost')
    global cursor
    cursor = connector.cursor()
    print ("Login success")
    return

def Generate(clicked):
    #connecting to mysql database .User will be prompted to enter password for mysql
    # passcode=input("Enter password for mysql : ")
    # connector=mysql.connector.connect(user='root',password=passcode,host='localhost',database='cricket')
    # cursor = connector.cursor()
    
    #creating database if they don't exist
    cursor.execute("drop database if exists cricket")
    cursor.execute("create database if not exists cricket")
    cursor.execute("use cricket")
    
    T=Tournament()
    T.load_data()
    T.generate_teams(8)
    
    
    
    cursor.execute("drop table if exists match_id")
    cursor.execute("create table match_id(match_no int(2) primary key)")
    cursor.execute("insert into match_id values(0)")
    
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
                mysql.connector.commit()
                i+=1
        cursor.close()

if __name__ == '__main__':
        
    tkWindow = Tk()
    tkWindow.title="Cricket Tournament"
    tkWindow.geometry("500x500")
        
    usernameLabel = Label(tkWindow, text="SQL User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="SQL Password").grid(row=1, column=0)  
    passcode = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=passcode, show='*').grid(row=1, column=1)  
   
    validateLogin = partial(validateLogin, username, passcode)
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)  
        
    tkWindow.mainloop()
        
        
