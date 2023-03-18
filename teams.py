import random

# List of player roles
player_roles = ['Bowler', 'Batsman', 'Wicket-Keeper', 'All-Rounder']

# List of player details
player_details = {
    'Bowler': ['Fast Bowler', 'Spin Bowler'],
    'Batsman': ['Left-Handed', 'Right-Handed'],
    'Wicket-Keeper': ['Agile Keeper', 'Accurate Thrower'],
    'All-Rounder': ['Left-Handed Batsman/Fast Bowler', 'Left-Handed Batsman/Spin Bowler', 'Right-Handed Batsman/Spin Bowler', 'Right-Handed Batsman/Fast Bowler']
}

# List of team names
team_names = {
    'Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 'Kolkata Knight Riders',
    'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad',
    'Deccan Gladiators', 'Jaipur Jaguars', 'Pune Panthers', 'Gujarat Lions',
    'Rising Pune Supergiant', 'Kochi Tuskers Kerala', 'Rising Pune Supergiants', 'Delhi Daredevils', 'Brisbane Heat', 'Adelaide Strikers', 'Melbourne Renegades', 'Melbourne Stars', 'Sydney Sixers',
    'Sydney Thunder', 'Perth Scorchers', 'Hobart Hurricanes', 'Big Bash Blasters', 'Canberra Calamities'
}

# List of player names
first_names = ['Adam', 'John', 'Mike', 'David', 'Steve', 'Daniel', 'Brian', 'Tyler', 'Kevin', 'Jake', 'Eric', 'Tom', 'Luke', 'Jeff', 'Frank', 'Charlie', 'Scott', 'Matt', 'Jack', 'Justin', 'Aarav', 'Aryan', 'Arjun', 'Amit', 'Aniket', 'Ankit', 'Alok', 'Anuj', 'Avinash', 'Aditya', 'Akash', 'Ajit', 'Bharat', 'Bhuvan', 'Brijesh', 'Chirag', 'Chetan', 'Dhruv', 'Dinesh', 'Deepak', 'Dhananjay', 'Dev', 'Devendra', 'Dharmesh', 'Darshan', 'Eklavya', 'Gaurav', 'Gopal', 'Ganesh', 'Hemant', 'Harsh', 'Harshal', 'Hrishikesh', 'Indrajeet', 'Ishaan', 'Jatin', 'Jagdish', 'Kartik', 'Kamal', 'Karan', 'Kunal', 'Krishna', 'Kumar', 'Lalit', 'Lakshya', 'Manish', 'Mukesh', 'Mayank', 'Mahesh', 'Mohan', 'Naveen', 'Nirav', 'Nishant', 'Om', 'Omkar', 'Prashant', 'Pramod', 'Pankaj', 'Parth', 'Pranav', 'Pradeep', 'Piyush', 'Rahul', 'Rakesh', 'Rohit', 'Rajesh', 'Rajendra', 'Sagar', 'Sandeep', 'Saurabh', 'Sanjay', 'Shubham', 'Shreyas', 'Sumit', 'Sushant', 'Siddharth', 'Sudhir', 'Suraj', 'Sushil', 'Sunil', 'Tanmay', 'Tarun', 'Uday', 'Umesh', 'Vikas', 'Vivek', 'Vinay', 'Vaibhav', 'Vikrant', 'Yash', 'Yuvraj']
last_names = ['Smith', 'Johnson', 'Brown', 'Lee', 'Wilson', 'Jones', 'Taylor', 'Clark', 'Wright', 'Walker', 'White', 'Green', 'Hall', 'Baker', 'Lewis', 'Cooper', 'Collins', 'Reed', 'Carter', 'Murphy', 'Agarwal', 'Bhagat', 'Bhargava', 'Chandra', 'Chopra', 'Choudhary', 'Dutta', 'Garg', 'Goyal', 'Gupta', 'Jain', 'Jha', 'Joshi', 'Kapoor', 'Khan', 'Kumar', 'Mahajan', 'Mehra', 'Mishra', 'Nair', 'Patel', 'Puri', 'Raj', 'Rao', 'Sahay', 'Saxena', 'Shah', 'Sharma', 'Singh', 'Sinha', 'Soni', 'Srivastava', 'Thakur', 'Trivedi', 'Verma']

# List of players
players = []

# Generate players with random details
for i in range(1, 441):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    age = random.randint(18, 40)
    role = random.choice(player_roles)
    details = random.choice(player_details[role])
    player = {'Name': first_name + ' ' + last_name, 'Age': age, 'Role': role, 'Details': details}
    players.append(player)

# Shuffle the list of players
random.shuffle(players)

# Generate 16 teams with 11 players each
num_teams = int(input("Enter number of teams: "))
teams = []
for name in random.sample(team_names, num_teams):
    team_players = []
    for i in range(4):
        player = random.choice([p for p in players if p['Role'] == 'Bowler'])
        team_players.append(player)
        players.remove(player)
    for i in range(4):
        player = random.choice([p for p in players if p['Role'] == 'Batsman'])
        team_players.append(player)
        players.remove(player)
    for i in range(2):
        player = random.choice([p for p in players if p['Role'] == 'All-Rounder'])
        team_players.append(player)
        players.remove(player)
    player = random.choice([p for p in players if p['Role'] == 'Wicket-Keeper'])
    team_players.append(player)
    players.remove(player)
    team_captain = random.choice(team_players)
    team = {'Team Name': name, 'Players': team_players, 'Captain': team_captain}
    teams.append(team)

# Print the list of teams and their players
# for team in teams:
#     print(team['Team Name'] + ':')
#     print('Captain: ' + team['Captain']['Name'] + '\n')
#     print('{:<20}{:<10}{:<20}{:<20}'.format('Name', 'Age', 'Role', 'Details'))
#     for player in team['Players']:
#         print('{:<20}{:<10}{:<20}{:<20}'.format(player['Name'], player['Age'], player['Role'], player['Details']))
#     print()
    
with open('teams.txt', 'w') as f:
    for team in teams:
        f.write(team['Team Name'] + ':\n')
        f.write('Captain: ' + team['Captain']['Name'] + '\n\n')
        f.write('{:<20}{:<10}{:<20}{:<20}\n'.format('Name', 'Age', 'Role', 'Details'))
        for player in team['Players']:
            f.write('{:<20}{:<10}{:<20}{:<20}\n'.format(player['Name'], player['Age'], player['Role'], player['Details']))
        f.write('\n')

