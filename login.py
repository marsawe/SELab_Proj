
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
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        # initializing frames to an empty array
        self.frames = {} 
        
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (login_page,gen_tourn,mainmenu,GuiSchedule,points_table) : 
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
        
        button2=ttk.Button(self,text = " Show Teams ",command = print_hello,width=15)
        button2.grid(row=4, column=0 , padx=10, pady=10)
        
        button3=ttk.Button(self,text = " Show Schedule ",command = partial(self.transition3,controller),width=15)
        button3.grid(row=5, column=0 , padx=10, pady=10)
        
        button4=ttk.Button(self,text = " Simulate Match ",command = partial(self.transition4),width=15)
        button4.grid(row=6, column=0 , padx=10, pady=10)
        
        button5=ttk.Button(self,text = " Points Table ",command = partial(self.transition5,controller),width=15)
        button5.grid(row=3, column=3 , padx=10, pady=10)
        
        button6=ttk.Button(self,text = " Match Scorecard ",command = print_hello,width=15)
        button6.grid(row=4, column=3 , padx=10, pady=10)
        
        button7=ttk.Button(self,text = " Team Stats ",command = print_hello,width=15)
        button7.grid(row=5, column=3 , padx=10, pady=10)
        
        button8=ttk.Button(self,text = " Tournament Stats ",command = print_hello,width=15)
        button8.grid(row=6, column=3 , padx=10, pady=10)
    
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
        
    
    def transition2(self,controller):
        controller.show_frame(transition2)
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
        controller.show_frame(transition6)
    def transition7(self,controller):
        controller.show_frame(transition7)
    def transition8(self,controller):
        controller.show_frame(transition8)
        
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
        
        
        
        
        
        controller.show_frame(mainmenu)
          

class GuiSchedule(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        show=tk.Button(self,text="Show Schedule",command=partial(self.showSchedule,controller))
        show.grid(row=0,column=0)
        self.parent=parent


        
    def showSchedule(self,controller):
        # myscrollbar=ttk.Scrollbar(self,orient="vertical")
        # myscrollbar.grid(column=8,sticky="ns")
        
        # self.canvas = tk.Canvas(self)
        # self.canvas.grid(row=1, column=0, sticky=tk.NSEW)

        # self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        # self.scrollbar.grid(row=0, column=7, sticky=tk.NS)
        # self.canvas.config(yscrollcommand=self.scrollbar.set)

        # self.inner_frame = tk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        
        headers = ["Match ID", "Date", "Time", "Stadium", "Venue", "Team 1", "Team 2"]
        for i, header in enumerate(headers):
            if i == 3 or i == 5 or i == 6:
                tk.Label(self, text=header, relief=tk.RIDGE, width=30).grid(row=1, column=i)
            else:
                tk.Label(self, text=header, relief=tk.RIDGE, width=10).grid(row=1, column=i)

        with open("schedule.txt", "r") as f:
            for i, line in enumerate(f, start=1):
                data = line.strip().split(",")
                match_id = str(i)
                tk.Label(self, text=match_id, relief=tk.RIDGE, width=10).grid(row=i+1, column=0)
                for j, value in enumerate(data):
                    if j == 2 or j == 4 or j == 5:
                        tk.Label(self, text=value.strip(), relief=tk.RIDGE, width=30).grid(row=i+1, column=j+1)
                    else:
                        tk.Label(self, text=value.strip(), relief=tk.RIDGE, width=10).grid(row=i+1, column=j+1)

        # self.inner_frame.update_idletasks()
        # self.canvas.config(scrollregion=self.canvas.bbox("all"))
        back=tk.Button(self,text="Back" , command=partial(controller.show_frame,mainmenu)).grid(row=i+2,column=0)

class points_table (tk.Frame) :
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        show=tk.Button(self,text="Show Points Table",command=partial(self.showPoints,controller))
        show.grid(row=0,column=0)
        self.parent=parent
    def showPoints(self,controller):
        cursor.execute("select * from points_table order by points desc")
        label_font=("Arial",20,"bold")
        
        tk.Label(self, text='Team', font=label_font, width=15, height=2, anchor='center').grid(row=1, column=0)
        tk.Label(self, text='Matches', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=1)
        tk.Label(self, text='Won', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=2)
        tk.Label(self, text='Drawn', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=3)
        tk.Label(self, text='Lost', font=label_font, width=10, height=2, anchor='center').grid(row=1, column=4)
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
        tk.Label(self,text="Total Matches Played : {}".format(num_match), width=15, height=2, anchor='center').grid(row=i+3,column=0)
        back=tk.Button(self,text="Back" , command=partial(controller.show_frame,mainmenu)).grid(row=i+4,column=0,columnspan=2,rowspan=2)
        

        
# Driver Code
app = tkinterApp()
app.mainloop()