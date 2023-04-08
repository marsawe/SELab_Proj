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
    cursor.execute("Create table match_{}_bowl2 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs int(2),runs int(3),wickets int(2),economy float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bat2".format(id))
    cursor.execute("Create table match_{}_bat2 (batting_position int(2) AUTO_INCREMENT PRIMARY KEY,batter varchar(30),runs int(3),balls int(3),fours int(2),sixes int(2),strike_rate float)".format(id))
    
    cursor.execute("drop table if exists match_{}_bowl1".format(id))
    cursor.execute("Create table match_{}_bowl1 (bowler_no int(2) AUTO_INCREMENT PRIMARY KEY,bowler varchar(30),overs int(2),runs int(3),wickets int(2),economy float)".format(id))
    

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
        container = tk.Frame(self,width=700,height=500) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # initializing frames to an empty array
        self.frames = {} 
        
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (login_page,gen_tourn,mainmenu,team_stats,tour_stats,show_team) : 
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
        
        validate_login=partial(self.validate_login,username,passcode,controller)
        login_button=ttk.Button(self,text = "Login",command = validate_login)
        login_button.grid(row=5, column=1)
        
    def validate_login(self,username,passcode,controller):
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
            
class mainmenu(tk.Frame) :
    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        #label of frame Layout
        label = ttk.Label(self, text ="Main Menu", font = LARGEFONT)
        
        #putting the grid in its place by using grid
        label.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        button1=ttk.Button(self,text = " Generate Schedule ",command =self.click1,width=15)
        button1.grid(row=3, column=0 , padx=10, pady=10)
        
        button2=ttk.Button(self,text = " Show Teams ",command = partial(self.transition2, controller),width=15)
        button2.grid(row=4, column=0 , padx=10, pady=10)
        
        button3=ttk.Button(self,text = " Show Schedule ",command = print_hello,width=15)
        button3.grid(row=5, column=0 , padx=10, pady=10)
        
        button4=ttk.Button(self,text = " Simulate Match ",command = self.transition4,width=15)
        button4.grid(row=6, column=0 , padx=10, pady=10)
        
        button5=ttk.Button(self,text = " Points Table ",command = print_hello,width=15)
        button5.grid(row=3, column=3 , padx=10, pady=10)
        
        button6=ttk.Button(self,text = " Match Scorecard ",command = print_hello,width=15)
        button6.grid(row=4, column=3 , padx=10, pady=10)
        
        button7=ttk.Button(self,text = " Team Stats ",command = partial(self.transition7, controller) ,width=15)
        button7.grid(row=5, column=3 , padx=10, pady=10)
        
        button8=ttk.Button(self,text = " Tournament Stats ",command = partial(self.transition8, controller),width=15)
        button8.grid(row=6, column=3 , padx=10, pady=10)
    
    def click1(self):
        
        cursor.execute("use cricket")
        
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
                team2=l[5].lstrip()
                team2=team2.strip("\n")
                sql="INSERT INTO schedule VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(i,date,time,stadium,venue,team1,team2)
                cursor.execute(sql)
                connector.commit()
                i+=1
        #End of creating a schedule table in database
        tkinter.messagebox.showinfo("Succesful", "The tounament schedule has been generated") 
        
    def transition7(self,controller):
        controller.show_frame(team_stats)
    def transition8(self,controller):
        controller.show_frame(tour_stats)
    def transition2(self,controller):
              controller.show_frame(show_team)
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
# =============================================================================
#     def transition5(self,controller):
#         controller.show_frame(points_table)
# =============================================================================
# =============================================================================
#     
#     def transition3(self,controller):
#         controller.show_frame(transition3)
#     def transition4(self,controller):
#         controller.show_frame(transition4)
#     def transition5(self,controller):
#         controller.show_frame(transition5)
#     def transition6(self,controller):
#         controller.show_frame(transition6)
#     
     
# =============================================================================
        

class gen_tourn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        numteams=tk.IntVar()
        e=tk.Entry(self, textvariable=numteams).grid(row=0,column=0)
        gen=tk.Button(self, text="Generate Tournament",command=partial(self.genTour,numteams,controller)).grid(row=1,column=0)
    def genTour(self,numteams,controller):
        if(int(numteams.get())==0):
            return		
        cursor.execute("drop database if exists cricket")
        cursor.execute("create database if not exists cricket")
        cursor.execute("use cricket")
        
        T.load_data()
        print(numteams)
        T.generate_teams(int(numteams.get()))
        
        cursor.execute("drop table if exists match_id")
        cursor.execute("create table match_id(match_no int(2) primary key)")
        cursor.execute("insert into match_id values(0)")
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
    
# Driver Code
app = tkinterApp()
app.mainloop()