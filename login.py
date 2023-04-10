import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import mysql.connector
from functools import partial
from schedule import Schedule
from teams import Tournament
from match import match

def simulate_match(id):
    # cursor=connector.cursor()
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
    
    #Creating the in sql for storing the match data
    
    cursor.execute("drop table if exists match_{}_bat1".format(id))
    cursor.execute("Create table match_{}_bat1 (batting_position int(2) PRIMARY KEY AUTO_INCREMENT,batter varchar(30),runs int(3),balls int(3),fours int(2),sixes int(2),strike_rate float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bowl2".format(id))
    cursor.execute("Create table match_{}_bowl2 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs float,runs int(3),wickets int(2),economy float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bat2".format(id))
    cursor.execute("Create table match_{}_bat2 (batting_position int(2) AUTO_INCREMENT PRIMARY KEY,batter varchar(30),runs int(3),balls int(3),fours int(2),sixes int(2),strike_rate float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bowl1".format(id))
    cursor.execute("Create table match_{}_bowl1 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs float,runs int(3),wickets int(2),economy float)".format(id))
    

    # team 1 batting stat and pushing them to the database
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
    
    #team 2 batting stat and pushing them to the database
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
            
    
    #updating points table based on the result of the match
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



def print_hello():
    print("Hello")

T = Tournament()
LARGEFONT =("Verdana", 25)
class tkinterApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        
        #creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # initializing frames to an empty array
        self.frames = {} 
        
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (login_page,gen_tourn,mainmenu,GuiSchedule,points_table,team_stats,tour_stats,show_team,scorecard,player_stats) : 
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        # frame=mainmenu(container,self)
        # self.frames[mainmenu]=frame
        # frame.grid(row=0,column=0,sticky="nsew")
            
        self.show_frame(login_page)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    
#first window login page
class login_page(tk.Frame) : 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        #label of frame Layout
        label = ttk.Label(self, text ="Login", font = LARGEFONT)
        
        #putting the grid in its place by using grid
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        #username label and text entry box
        usernameLabel = ttk.Label(self, text="SQL User Name").grid(row=1, column=0)
        username = tk.StringVar()
        usernameEntry = ttk.Entry(self, textvariable=username).grid(row=1, column=1)  

        #password label and password entry box
        passwordLabel = ttk.Label(self,text="SQL Password").grid(row=2, column=0)  
        passcode = tk.StringVar()
        passwordEntry = ttk.Entry(self, textvariable=passcode, show='*').grid(row=2, column=1) 
        
        validate_login=partial(self.validate_login,username,passcode,controller,passwordEntry,usernameEntry)
        login_button=ttk.Button(self,text = "Login",command = validate_login)
        login_button.grid(row=5, column=1)
        
    def validate_login(self,username,passcode,controller,passwordEntry,usernameEntry):
        try :
            global connector 
            connector=mysql.connector.connect(user=username.get(),password=passcode.get(),host='localhost')
            global usr
            usr=username.get()
            global passcode_
            passcode_ = passcode.get()
            global cursor
            cursor = connector.cursor()
            print("Connection Successful")
            # creating the link to next page
            controller.show_frame(gen_tourn)
            
        except mysql.connector.Error as err:
            error_label=ttk.Label(self,text="Invalid Username or Password")
            error_label.grid(row=6,column=1)
            usernameEntry.delete(0, 'end')
            passwordEntry.delete(0, 'end')
            
            
class mainmenu(tk.Frame) :
    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent=parent

        #label of frame Layout
        label = ttk.Label(self, text ="Main Menu", font = LARGEFONT)
        
        #putting the grid in its place by using grid
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        button1=ttk.Button(self,text = " Generate Schedule ",command =self.click1,width=15)
        button1.grid(row=3, column=0 , padx=10, pady=10)
        
        button2=ttk.Button(self,text = " Show Teams ",command = partial(self.transition2, controller),width=15)
        button2.grid(row=4, column=0 , padx=10, pady=10)
        
        button3=ttk.Button(self,text = " Show Schedule ",command = partial(self.transition3,controller),width=15)
        button3.grid(row=5, column=0 , padx=10, pady=10)
        
        button4=ttk.Button(self,text = " Simulate Match ",command = partial(self.transition4),width=15)
        button4.grid(row=6, column=0 , padx=10, pady=10)
        
        button5=ttk.Button(self,text = " Points Table ",command = partial(self.transition5,controller),width=15)
        button5.grid(row=3, column=3 , padx=10, pady=10)
        
        button6=ttk.Button(self,text = " Match Scorecard ",command = partial(self.transition6, controller),width=15)
        button6.grid(row=4, column=3 , padx=10, pady=10)
        
        button7=ttk.Button(self,text = " Team Stats ",command = partial(self.transition7, controller),width=15)
        button7.grid(row=5, column=3 , padx=10, pady=10)
        
        button8=ttk.Button(self,text = " Tournament Stats ",command = partial(self.transition8, controller),width=15)
        button8.grid(row=6, column=3 , padx=10, pady=10)
        button9=ttk.Button(self,text = " Player Stats ",command = partial(self.transition9, controller),width=15)
        button9.grid(row=7, column=3 , padx=10, pady=10)
    
    def parent(self) :
        return self.parent
    
    def click1(self):
        
        cursor.execute("use cricket")
        
        schedule=Schedule()
            
        #creating schedule table in database
        cursor.execute("drop table if exists schedule")
        cursor.execute("create table schedule(Match_no int(2) , date varchar(15), time varchar(10),stadium varchar(50) , venue varchar(20), team1 varchar(30), team2 varchar(30), primary key(Match_no))")
        #creating points table in database
        cursor.execute("drop table if exists points_table")
        cursor.execute("create table points_table(team varchar(30),played int(2),won int(2),lost int(2),drawn int(2),points int(2),last_5_matches varchar(5))")
        
        cursor.execute("drop table if exists match_id")
        cursor.execute("create table match_id(match_no int(2) primary key)")
        cursor.execute("insert into match_id values(0)")
        
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
        
        p=[]
        global d
        d={}
        with open("schedule.txt","r") as f :
            i=1
            for x in f : 
                l=x.split(",")
                
                date=l[0].strip()
                time=l[1].strip()
                stadium=l[2].strip()
                venue=l[3].strip()
                team1=l[4].strip()
                team2=l[5].lstrip()
                team2=team2.strip("\n")
                t1=""
                t2=""
                for char in team1 :
                    if char.isupper() :
                        t1+=char
                for char in team2 :
                    if char.isupper() :
                        t2+=char
                p.append(t1+" vs "+t2)
                d[t1+" vs "+t2]=i
                sql="INSERT INTO schedule VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(i,date,time,stadium,venue,team1,team2)
                cursor.execute(sql)
                connector.commit()
                i+=1
        gp=self.parent.master
        
        gp.frames[scorecard].options=p
        gp.frames[scorecard].clicked.set(gp.frames[scorecard].options[0])
        gp.frames[scorecard].dropDown=tk.OptionMenu(gp.frames[scorecard],gp.frames[scorecard].clicked, *gp.frames[scorecard].options)
        gp.frames[scorecard].dropDown.grid(row = 1, column = 0)
        
        #End of creating a schedule table in database
        tkinter.messagebox.showinfo("Succesful", "The tounament schedule has been generated") 
        
    
    def transition2(self,controller):
        controller.show_frame(show_team)
    def transition3(self,controller):
        controller.show_frame(GuiSchedule)
    def transition4(self):
        
        top=tk.Toplevel()
        top.geometry("700x300")
        top.title("Simulate Match")
        cursor.execute("select match_no from match_id")
        num_match=cursor.fetchone()[0]
        tk.Label(top,text="{} matches has been simulated .".format(num_match)).grid(row=0,column=0,padx=10,pady=10)
        tk.Label(top,text="Enter how many matches to simulate").grid(row=1,column=0,padx=10,pady=10)
        sim_num=tk.IntVar()
        e=tk.Entry(top,textvariable=sim_num).grid(row=1,column=1)
        simulate_button=tk.Button(top,text="Simulate",command=partial(self.simulate,sim_num,top)).grid(row=2,column=1)
    def transition5(self,controller):
        controller.show_frame(points_table)
    def transition6(self,controller):
        controller.show_frame(scorecard)
    def transition7(self,controller):
        controller.show_frame(team_stats)
    def transition8(self,controller):
        controller.show_frame(tour_stats)
    def transition9(self,controller):
        controller.show_frame(player_stats)
        
    def simulate(self,sim_num,top):
        cursor.execute("select max(Match_no) from schedule")
        num_match=cursor.fetchone()[0]
        if(int(sim_num.get())<= 0 or int(sim_num.get())>num_match):
            tk.Label(top,text="Enter a valid number").grid(row=3,column=1)
            return
        cursor.execute("select max(match_no) from match_id")
        match_id=cursor.fetchone()[0]
        if(match_id+int(sim_num.get())>num_match):
            if(num_match-match_id>0):
                tk.Label(top,text="You can simulate only {} more matches".format(num_match-match_id)).grid(row=3,column=1)
            else : 
                tk.Label(top,text="All the matches have been simulated").grid(row=3,column=1)
            return
        cursor.execute("Update match_id set match_no=match_no+{}".format(int(sim_num.get())))
        connector.commit()
        for match_num in range(match_id+1,match_id+int(sim_num.get())+1) :
            simulate_match(match_num)
        tkinter.messagebox.showinfo("Succesful", "The matches have been simulated")
        top.destroy()
    
        
class gen_tourn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        usernameLabel = ttk.Label(self, text="Number of teams ").grid(row=1, column=0)
        global numteams
        numteams=tk.IntVar()
        e=tk.Entry(self, textvariable=numteams).grid(row=1,column=1)
        gen=tk.Button(self, text="Generate Tournament",command=partial(self.genTour,numteams,controller)).grid(row=2,column=1)
    def genTour(self,numteams,controller):
        try:
            if(int(numteams.get())<=1 or int(numteams.get())>26):
                tk.Label(self,text="Enter a valid number of teams\n(between 2 and 26)").grid(row=3,column=1)
                return
        except:
            tk.Label(self,text="Enter a valid number of teams\n(between 2 and 26)").grid(row=3,column=1)
            return
				
        cursor.execute("drop database if exists cricket")
        cursor.execute("create database if not exists cricket")
        cursor.execute("use cricket")
        
        
        
        T.load_data()
        T.generate_teams(int(numteams.get()))
        
        
        parent_name = self.winfo_parent()
        parent = self._nametowidget(parent_name)
        gp=parent._nametowidget(parent.winfo_parent())
        gp.frames[team_stats].options=[team.name for team in T.teams]
        gp.frames[team_stats].clicked.set(gp.frames[team_stats].options[0])
        gp.frames[team_stats].dropDown=tk.OptionMenu(gp.frames[team_stats],gp.frames[team_stats].clicked, *gp.frames[team_stats].options)
        gp.frames[team_stats].dropDown.grid(row = 0, column = 1)
        gp.frames[show_team].options=[team.name for team in T.teams]
        gp.frames[show_team].clicked.set(gp.frames[show_team].options[0])
        gp.frames[show_team].dropDown=tk.OptionMenu(gp.frames[show_team],gp.frames[show_team].clicked, *gp.frames[show_team].options)
        gp.frames[show_team].dropDown.grid(row = 0, column = 1)
        gp.frames[player_stats].options=[team.name for team in T.teams]
        gp.frames[player_stats].clicked.set(gp.frames[player_stats].options[0])
        gp.frames[player_stats].dropDown=tk.OptionMenu(gp.frames[player_stats],gp.frames[player_stats].clicked, *gp.frames[player_stats].options)
        gp.frames[player_stats].dropDown.grid(row = 0, column = 1)
        
        
        
        controller.show_frame(mainmenu)
          
class team_stats(tk.Frame):
    def __init__(self, parent, controller):           
        tk.Frame.__init__(self,parent)
        self.clicked=tk.StringVar()
        self.options=["idk"]
        Output = tk.Text(self,height=7)
        Output.grid(row=0,column=3)
        statsButton = tk.Button(self, text = "Show stats" , command = partial(self.dispStats,self.clicked,Output))
        statsButton.grid(row = 0, column = 2)
        backButton=tk.Button(self, text = "Back", command = partial(controller.show_frame,mainmenu))
        backButton.grid(row=1,column=0)
        
        
    def dispStats(self,clicked,Output):
        Output.delete("1.0","end")
        cursor.execute("select played from points_table where team = \"{}\"".format(str(clicked.get())))
        played = cursor.fetchone()
        Output.insert(tk.END,"Matches played: " + str(played)[1:-2]+'\n')         
        cursor.execute("select won from points_table where team = \"{}\"".format(clicked.get()))
        won = cursor.fetchone()
        Output.insert(tk.END,"Matches won: " + str(won)[1:-2]+'\n')    
        cursor.execute("select lost from points_table where team = \"{}\"".format(clicked.get()))
        lost = cursor.fetchone()
        Output.insert(tk.END,"Matches lost: " + str(lost)[1:-2]+'\n')
        cursor.execute("select drawn from points_table where team = \"{}\"".format(clicked.get()))
        drawn = cursor.fetchone()
        Output.insert(tk.END,"Matches drawn: " + str(drawn)[1:-2]+'\n')
        cursor.execute("select last_5_matches from points_table where team = \"{}\"".format(clicked.get()))
        l5 = cursor.fetchone()
        Output.insert(tk.END,"Last 5 matches: " + str(l5)[1:-2]+'\n')
        for team in T.teams :
            if team.name==clicked.get():
                t=team
        tsco=t.top_scorer()
        twic=t.top_wickettaker()
        Output.insert(tk.END,"Top run-scorer: " + tsco.first_name + ' ' + tsco.last_name +":"+ str(tsco.runs_scored)+'\n')
        Output.insert(tk.END,"Top wicket-taker: " + twic.first_name + ' ' + twic.last_name+":"+ str(twic.wickets) +'\n')
            

class tour_stats(tk.Frame):
    def __init__(self, parent, controller):           
        tk.Frame.__init__(self,parent)
        Output1 = tk.Text(self,height=6,width=25)
        Output1.grid(row=0,column=2)
        Output2 = tk.Text(self,height=6,width=25)
        Output2.grid(row=0,column=3)
        statsButton = tk.Button(self, text = "Show stats" , command = partial(self.dispStats,Output1,Output2))
        statsButton.grid(row = 0, column = 1)
        backButton=tk.Button(self, text = "Back", command = partial(controller.show_frame,mainmenu))
        backButton.grid(row=1,column=0)
    def dispStats(self,Output1,Output2):
        Output1.delete("1.0","end")
        Output2.delete("1.0","end")
        T.calc_stats()
        Output1.insert(tk.END,"Top 5 runscorers\n")
        for keys, values in T.sorted_runs.items():
            Output1.insert(tk.END,keys+":"+str(values)+"\n")
        Output2.insert(tk.END,"Top 5 wickettakers\n")
        for keys, values in T.sorted_wickets.items():
            Output2.insert(tk.END,keys+":"+str(values)+"\n")


class show_team(tk.Frame):
    def __init__(self, parent, controller):           
        tk.Frame.__init__(self,parent)
        self.clicked=tk.StringVar()
        self.options=["idk"]
        Output = tk.Text(self,height=15,width=90)
        Output.grid(row=0,column=3)
        detailsButton = tk.Button(self, text = "Show details" , command = partial(self.dispStats,self.clicked,Output))
        detailsButton.grid(row = 0, column = 2)
        backButton=tk.Button(self, text = "Back", command = partial(controller.show_frame,mainmenu))
        backButton.grid(row=1,column=0)
    def dispStats(self,clicked,Output):
        Output.delete("1.0","end")
        for team in T.teams :
            if team.name==clicked.get():
                t=team
        Output.insert(tk.END,t.__str__())


class scorecard(tk.Frame):
    def __init__(self, parent, controller):           
        tk.Frame.__init__(self,parent)
        self.clicked=tk.StringVar()
        self.options=["idk"]
        Output=tk.Text(self,height=5)
        Output.tag_configure("center", justify='center')
        Output.grid(row=0,column=3,columnspan=2)
        Output1=tk.Text(self,height=15)
        Output1.grid(row=1,column=3)
        Output2=tk.Text(self,height=15)
        Output2.grid(row=1,column=4)
        Output3=tk.Text(self,height=15)
        Output3.grid(row=2,column=3)
        Output4=tk.Text(self,height=15)
        Output4.grid(row=2,column=4)
        detailsButton = tk.Button(self, text = "Show scorecard" , command = partial(self.dispStats,self.clicked,Output,Output1,Output2,Output3,Output4))
        detailsButton.grid(row = 1, column = 1)
        backButton=tk.Button(self, text = "Back", command = partial(controller.show_frame,mainmenu))
        backButton.grid(row=2,column=0)
    def dispStats(self,clicked,Output,Output1,Output2,Output3,Output4):
        Output.delete("1.0","end")
        Output1.delete("1.0","end")
        Output2.delete("1.0","end")
        Output3.delete("1.0","end")
        Output4.delete("1.0","end")
        team1,team2=str(clicked.get()).split(" vs ")
        cursor.execute("select SUM(runs) from {}".format("match_"+str(d[clicked.get()])+"_bat1"))
        team1bat=cursor.fetchone()[0]
        cursor.execute("select SUM(runs) from {}".format("match_"+str(d[clicked.get()])+"_bat2"))
        team2bat=cursor.fetchone()[0]
        cursor.execute("select SUM(wickets) from {}".format("match_"+str(d[clicked.get()])+"_bowl1"))
        team1bowl=cursor.fetchone()[0]
        cursor.execute("select SUM(wickets) from {}".format("match_"+str(d[clicked.get()])+"_bowl2"))
        team2bowl=cursor.fetchone()[0]
        
        Output.insert(tk.END,"\t\t\t\tMatch: "+str(d[clicked.get()])+'\n\t' + team1 +'\t' +str(team1bat) + '/' + str(team2bowl) + '\t\t\t\t' + str(team2bat) + '/' + str(team1bowl) + '\t'+team2+'\n\t\t\t   ')
        if team1bat>team2bat:
            Output.insert(tk.END,team1+" won by "+str(team1bat-team2bat)+" runs\n")
        elif team1bat<team2bat:
            Output.insert(tk.END,team2+" won by "+str(10-team1bowl)+" wickets\n")
        else:
            Output.insert(tk.END,"Match drawn\n")
        

        cursor.execute("select * from {}".format("match_"+str(d[clicked.get()])+"_bat1"))
        op=cursor.fetchall()
        
        Output1.insert(tk.END,team1 +" batting\nS.No.\tName\t\t\tRuns\tBalls\tFours\tSixes\tStrike rate\n")
        for player in op:
            i=0
            for stat in player:
                if(i==0):
                    Output1.insert(tk.END,str(stat)+' ')
                elif(i==2):
                    Output1.insert(tk.END,'\t\t\t'+str(stat)+' ')
                else:
                    Output1.insert(tk.END,'\t'+str(stat)+' ')
                i+=1
            Output1.insert(tk.END,'\n')
        cursor.execute("select * from {}".format("match_"+str(d[clicked.get()])+"_bowl2"))
        op=cursor.fetchall()
        Output2.insert(tk.END,team2+" bowling\nS.No.\tName\t\t\tOvers\tRuns\tWickers\tEconomy\n")
        for player in op:
            i=0
            for stat in player:
                if(i==0):
                    Output2.insert(tk.END,str(stat)+' ')
                elif(i==2):
                    Output2.insert(tk.END,'\t\t\t'+str(stat)+' ')
                else:
                    Output2.insert(tk.END,'\t'+str(stat)+' ')
                i+=1
            Output2.insert(tk.END,'\n')
        cursor.execute("select * from {}".format("match_"+str(d[clicked.get()])+"_bat2"))
        op=cursor.fetchall()
        Output3.insert(tk.END,team2+" batting\nS.No.\tName\t\t\tRuns\tBalls\tFours\tSixes\tStrike rate\n")
        for player in op:
            i=0
            for stat in player:
                if(i==0):
                    Output3.insert(tk.END,str(stat)+' ')
                elif(i==2):
                    Output3.insert(tk.END,'\t\t\t'+str(stat)+' ')
                else:
                    Output3.insert(tk.END,'\t'+str(stat)+' ')
                i+=1
            Output3.insert(tk.END,'\n')
        cursor.execute("select * from {}".format("match_"+str(d[clicked.get()])+"_bowl1"))
        op=cursor.fetchall()
        Output4.insert(tk.END,team1+" bowling\nS.No.\tName\t\t\tOvers\tRuns\tWickers\tEconomy\n")
        for player in op:
            i=0
            for stat in player:
                if(i==0):
                    Output4.insert(tk.END,str(stat)+' ')
                elif(i==2):
                    Output4.insert(tk.END,'\t\t\t'+str(stat)+' ')
                else:
                    Output4.insert(tk.END,'\t'+str(stat)+' ')
                i+=1
            Output4.insert(tk.END,'\n')

class GuiSchedule(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        show = tk.Button(self, text="Show Schedule", command=partial(self.show_schedule,controller))
        show.grid(row=0, column=0)
        self.parent = parent
        self.controller = controller
        
    def show_schedule(self, controller):
        schedule = tk.Text(self, height=40, width=155)
        schedule.grid(row=1, column=0, columnspan=8)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=schedule.yview)
        scrollbar.grid(row=1, column=8, sticky="ns")
        schedule.config(yscrollcommand=scrollbar.set)
        
        headers = ["Match ID", "Date", "Time", "Stadium", "Venue", "Team 1", "Team 2"]
        schedule.insert(tk.END, "{:<10} {:<10} {:<6} {:<52} {:<12} {:<29} {:<29}\n\n".format(*headers))

        with open('schedule.txt', "r") as f:
            for i, line in enumerate(f, start=1):
                data = line.strip().split(",")
                match_id = str(i)
                schedule.insert(tk.END, "{:<10} {:<10} {:<5} {:<50} {:<10} {:<28} {:<28}\n".format(match_id, *data))

        back = tk.Button(self, text="Back", command=partial(controller.show_frame,mainmenu))
        back.grid(row=2, column=0)
class points_table (tk.Frame) :
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        show=tk.Button(self,text="Show Points Table",command=partial(self.showPoints,controller))
        show.grid(row=0,column=0)
        self.parent=parent
    def showPoints(self,controller):
        cursor.execute("select * from points_table order by points desc")
        if numteams.get() <= 10 :
            label_font=("Arial",20,"bold")
        elif numteams.get() <= 15 :
            label_font=("Arial",15,"bold")
        elif numteams.get() <= 20 :
            label_font=("Arial",10,"bold")
        else :
            label_font=("Arial",8,"bold")
        
        tk.Label(self, text='Team', font=label_font, width=15, height=2, anchor='center').grid(row=1, column=0)
        tk.Label(self, text='Matches', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=1)
        tk.Label(self, text='Won', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=2)
        tk.Label(self, text='Lost', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=3)
        tk.Label(self, text='Drawn', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=4)
        tk.Label(self, text='Points', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=5)
        tk.Label(self, text='Last 5 matches', font=label_font, width=15, height=2, anchor='center').grid(row=1, column=6)
        
        points_data=cursor.fetchall()
        
        for i ,row in enumerate(points_data , start=1):
            team=""
            for char in row[0] :
                if char.isupper() :
                    team+=char     
            tk.Label(self, text=team, font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=0)
            tk.Label(self, text=row[1], font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=1)
            tk.Label(self, text=row[2], font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=2)
            tk.Label(self, text=row[3], font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=3)
            tk.Label(self, text=row[4], font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=4)
            tk.Label(self, text=row[5], font=label_font, width=10, height=2, anchor='center').grid(row=i+2, column=5)
            tk.Label(self, text=row[6], font=label_font, width=15, height=2, anchor='center').grid(row=i+2, column=6)
        cursor.execute("select match_no from match_id")
        num_match=cursor.fetchone()[0]
        tk.Label(self,text="*Total Matches \nPlayed : {}".format(num_match), width=15, height=2, anchor='center').grid(row=i+3,column=0)
        back=tk.Button(self,text="Back" , command=partial(controller.show_frame,mainmenu)).grid(row=i+4,column=0,columnspan=2,rowspan=2)
        


class player_stats(tk.Frame):
    def __init__(self, parent, controller):  
        self.var = tk.StringVar()
        self.var.set('')         
        tk.Frame.__init__(self,parent)
        self.clicked=tk.StringVar()
        self.options=["idk"]
        self.clicked2=tk.StringVar()
        self.options2=["idk"]
        Output = tk.Text(self,height=15,width=40)
        Output.grid(row=2,column=1,columnspan=3)
        tdetailsButton = tk.Button(self, text = "Select team" , command = partial(self.dispStats,self.clicked,Output))
        tdetailsButton.grid(row = 1, column = 1)
        backButton=tk.Button(self, text = "Back", command = partial(controller.show_frame,mainmenu))
        backButton.grid(row=2,column=0)
        self.player1=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,1,Output))
        self.player1.grid(row = 0, column=7)
        self.player2=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,2,Output))
        self.player2.grid(row = 0, column=2)
        self.player3=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,3,Output))
        self.player3.grid(row = 0, column=3)
        self.player4=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,4,Output))
        self.player4.grid(row = 0, column=4)
        self.player5=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,5,Output))
        self.player5.grid(row = 0, column=5)
        self.player6=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,6,Output))
        self.player6.grid(row = 0, column=6)
        self.player7=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,7,Output))
        self.player7.grid(row = 1, column=6)
        self.player8=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,8,Output))
        self.player8.grid(row = 1, column=2)
        self.player9=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,9,Output))
        self.player9.grid(row = 1 ,column=3)
        self.player10=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,10,Output))
        self.player10.grid(row = 1, column=4)
        self.player11=tk.Button(self, text = "Select a team first", command = partial(self.dispPlayer,11,Output))
        self.player11.grid(row = 1, column=5)
        
    def dispStats(self,clicked,Output):
        for team in T.teams :
            if team.name==clicked.get():
                self.t=team
        self.player1['text']=self.t.players[0].first_name+ ' '+ self.t.players[0].last_name
        self.player2['text']=self.t.players[1].first_name+ ' '+ self.t.players[1].last_name
        self.player3['text']=self.t.players[2].first_name+ ' '+ self.t.players[2].last_name
        self.player4['text']=self.t.players[3].first_name+ ' '+ self.t.players[3].last_name
        self.player5['text']=self.t.players[4].first_name+ ' '+ self.t.players[4].last_name
        self.player6['text']=self.t.players[5].first_name+ ' '+ self.t.players[5].last_name
        self.player7['text']=self.t.players[6].first_name+ ' '+ self.t.players[6].last_name
        self.player8['text']=self.t.players[7].first_name+ ' '+ self.t.players[7].last_name
        self.player9['text']=self.t.players[8].first_name+ ' '+ self.t.players[8].last_name
        self.player10['text']=self.t.players[9].first_name+ ' '+ self.t.players[9].last_name
        self.player11['text']=self.t.players[10].first_name+ ' '+ self.t.players[10].last_name
        
    def dispPlayer(self, num, Output):
        p=self.t.players[num-1]
        Output.delete("1.0","end")
        Output.insert(tk.END,"Name:" + str(p.first_name)+' '+p.last_name+'\n')
        Output.insert(tk.END,"Age:" + str(p.age)+'\n')
        Output.insert(tk.END,"Team:" + str(self.t.name)+'\n')
        Output.insert(tk.END,"Role:" + str(p.role)+'\n')
        Output.insert(tk.END,"Details:" + str(p.details)+'\n')
        Output.insert(tk.END,"Runs scored:" + str(p.runs_scored)+'\n')
        Output.insert(tk.END,"Balls faced:" + str(p.balls_faced)+'\n')
        Output.insert(tk.END,"Wickets taken:" + str(p.wickets)+'\n')
        Output.insert(tk.END,"Overs bowled:" + str(p.overs)+'\n')
        Output.insert(tk.END,"Runs conceded:" + str(p.runs_conceded)+'\n')
      
# Driver Code
app = tkinterApp()
app.mainloop()