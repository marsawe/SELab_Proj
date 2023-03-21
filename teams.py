import random

class Player:
    
    def __init__(self, first_name, last_name, age, role, details):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.role = role
        self.details = details
        self.runs_scored=0
        self.balls_faced=0
        self.wickets=0
        self.overs=0
        self.runs_conceded=0
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})'
    
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.captain = None
        
    def add_player(self, player):
        self.players.append(player)

    def set_captain(self, player):
        self.captain = player

    def __str__(self):
        output = f'{self.name}: \n'
        output += f'Captain: {self.captain}\n\n'
        output += '{:<20}{:<10}{:<20}{:<20}\n'.format(
            'Name', 'Age', 'Role', 'Details')
        for player in self.players:
            output += '{:<20}{:<10}{:<20}{:<20}\n'.format(
                player.first_name + ' ' + player.last_name, player.age, player.role, player.details)
        output += '\n'
        return output


class Tournament:

    def __init__(self):
        self.teams = []
        self.players = []
        self.player_roles = ['Bowler', 'Batsman',
                             'Wicket-Keeper', 'All-Rounder']
        self.player_details = {
            'Bowler': ['Fast Bowler', 'Spin Bowler'],
            'Batsman': ['Left-Handed', 'Right-Handed'],
            'Wicket-Keeper': ['Agile Keeper', 'Accurate Thrower'],
            'All-Rounder': ['Left-Handed Batsman/Fast Bowler', 'Left-Handed Batsman/Spin Bowler', 'Right-Handed Batsman/Spin Bowler', 'Right-Handed Batsman/Fast Bowler']
        }

    def add_team(self, team):
        self.teams.append(team)

    def add_player(self, player):
        self.players.append(player)

    def generate_teams(self, num_teams):
        used_names = set()
        for i in range(num_teams):
            while True:
                team_name = random.choice(self.team_names)
                if team_name not in used_names:
                    used_names.add(team_name)
                    break
            team = Team(team_name)
            self.add_team(team)
            team_players = []
            for i in range(4):
                player = random.choice(
                    [p for p in self.players if p.role == 'Batsman'])
                team_players.append(player)
                self.players.remove(player)
            player = random.choice(
                [p for p in self.players if p.role == 'Wicket-Keeper'])
            team_players.append(player)
            self.players.remove(player)
            for i in range(2):
                player = random.choice(
                    [p for p in self.players if p.role == 'All-Rounder'])
                team_players.append(player)
                self.players.remove(player)
            for i in range(4):
                player = random.choice(
                    [p for p in self.players if p.role == 'Bowler'])
                team_players.append(player)
                self.players.remove(player)
            team_captain = random.choice(team_players)
            team.set_captain(team_captain)
            for player in team_players:
                team.add_player(player)

    def print_teams(self):
        for team in self.teams:
            print(team)

    def save_teams(self, teams, filename):
        with open(filename, 'w') as f:
            for team in teams:
                f.write(team.name + ':\n')
                f.write('Captain: ' + team.captain.first_name +
                        ' ' + team.captain.last_name + '\n\n')
                f.write('{:<20}{:<10}{:<20}{:<20}\n'.format(
                    'Name', 'Age', 'Role', 'Details'))
                for player in team.players:
                    f.write('{:<20}{:<10}{:<20}{:<20}\n'.format(
                        player.first_name + ' ' + player.last_name, player.age, player.role, player.details))
                f.write('\n')
        print(f'The teams have been saved to {filename} successfully!')

    def load_data(self):
        with open('first_names.txt') as f:
            self.first_names = f.read().split(', ')
        with open('last_names.txt') as f:
            self.last_names = f.read().split(', ')
        with open('team_names.txt') as f:
            self.team_names = f.read().split(', ')
        for i in range(1, 420):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            age = random.randint(18, 40)
            role = random.choice(self.player_roles)
            details = random.choice(self.player_details[role])
            player = Player(first_name, last_name, age, role, details)
            self.add_player(player)


if __name__ == '__main__':
    tournament = Tournament()
    tournament.load_data()
    num_teams = int(input("Enter number of teams: "))
    teams = tournament.generate_teams(num_teams)
    tournament.print_teams()
    tournament.save_teams(tournament.teams, 'teams.txt')

