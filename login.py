
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import mysql.connector
from functools import partial
from schedule import Schedule
from teams import Tournament

def print_hello():
    print("Hello")

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
        for F in (login_page,gen_tourn,mainmenu) : 
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
        
        button2=ttk.Button(self,text = " Show Teams ",command = print_hello,width=15)
        button2.grid(row=4, column=0 , padx=10, pady=10)
        
        button3=ttk.Button(self,text = " Show Schedule ",command = print_hello,width=15)
        button3.grid(row=5, column=0 , padx=10, pady=10)
        
        button4=ttk.Button(self,text = " Simulate Match ",command = print_hello,width=15)
        button4.grid(row=6, column=0 , padx=10, pady=10)
        
        button5=ttk.Button(self,text = " Points Table ",command = print_hello,width=15)
        button5.grid(row=3, column=3 , padx=10, pady=10)
        
        button6=ttk.Button(self,text = " Match Scorecard ",command = print_hello,width=15)
        button6.grid(row=4, column=3 , padx=10, pady=10)
        
        button7=ttk.Button(self,text = " Team Stats ",command = print_hello,width=15)
        button7.grid(row=5, column=3 , padx=10, pady=10)
        
        button8=ttk.Button(self,text = " Tournament Stats ",command = print_hello,width=15)
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
                team2=l[5].strip("\n")
                sql="INSERT INTO schedule VALUES ({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(i,date,time,stadium,venue,team1,team2)
                cursor.execute(sql)
                connector.commit()
                i+=1
        #End of creating a schedule table in database
        tkinter.messagebox.showinfo("Succesful", "The tounament schedule has been generated") 
        
    
    def transition2(self,controller):
        controller.show_frame(transition2)
    def transition3(self,controller):
        controller.show_frame(transition3)
    def transition4(self,controller):
        controller.show_frame(transition4)
    def transition5(self,controller):
        controller.show_frame(transition5)
    def transition6(self,controller):
        controller.show_frame(transition6)
    def transition7(self,controller):
        controller.show_frame(transition7)
    def transition8(self,controller):
        controller.show_frame(transition8)
        
            
    
        
class gen_tourn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        usernameLabel = ttk.Label(self, text="Number of teams ").grid(row=1, column=0)
        numteams=tk.IntVar()
        e=tk.Entry(self, textvariable=numteams).grid(row=1,column=1)
        gen=tk.Button(self, text="Generate Tournament",command=partial(self.genTour,numteams,controller)).grid(row=2,column=1)
    def genTour(self,numteams,controller):
        if(int(numteams.get())==0):
            return
				
        cursor.execute("drop database if exists cricket")
        cursor.execute("create database if not exists cricket")
        cursor.execute("use cricket")
        
        global T
        T = Tournament()
        T.load_data()
        T.generate_teams(int(numteams.get()))
        
        cursor.execute("drop table if exists match_id")
        cursor.execute("create table match_id(match_no int(2) primary key)")
        cursor.execute("insert into match_id values(0)")
        
        controller.show_frame(mainmenu)
          
            
        
            
        
# Driver Code
app = tkinterApp()
app.mainloop()