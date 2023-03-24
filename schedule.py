import random
from datetime import datetime, timedelta


class Schedule:
    def __init__(self):
        self.matches = []
        self.teams = []
        self.venues = []

    def add_match(self, match):
        if len(match) == 2:
            home, away = match
            venue = ""
            date = ""
            time = ""
            self.matches.append((home, away, venue, date, time))
        else:
            self.matches.append(match)

    def add_team(self, team):
        self.teams.append(team)

    def add_venue(self, venue):
        self.venues.append(venue)

    def generate_schedule(self):
        random.shuffle(self.teams)

        global match_count
        match_count = len(self.teams) * (len(self.teams) - 1) // 2
        mid_point = len(self.teams) // 2

        for i in range(match_count):
            round = []
            for j in range(mid_point):
                home = self.teams[j]
                away = self.teams[-j-1]
                if i % 2 == 0:
                    round.append((home, away))
                else:
                    round.append((away, home))
            self.add_round(round)
            self.teams.insert(1, self.teams.pop())

    def add_round(self, round):
        for match in round:
            self.add_match(match)

    def print_schedule(self, filename):
        with open(filename, 'w') as f:
            date = datetime(2023, 4, 14)
            for i in range(len(self.matches)):
                if i >= match_count:
                    break
                home, away, venue, date_str, time_str = self.matches[i]
                if i % 2 == 0:
                    date += timedelta(days=1)
                    if date.weekday() == 5 or date.weekday() == 6:
                        time = datetime.strptime(random.choice(['18:00', '22:00']), "%H:%M").strftime("%H%M")
                    else:
                        time = datetime.strptime('22:00', "%H:%M").strftime("%H%M")

                venue = random.choice(self.venues)
                while (date.strftime("%d-%m-%Y"), venue) in [(x[3], x[2]) for x in self.matches if x]:
                    venue = random.choice(self.venues)

                self.matches[i] = (home, away, venue, date.strftime("%d-%m-%Y"), time)
                f.write(f"{date.strftime('%d-%m-%Y')}, {time}, {venue}, {home} ,{away}\n")



if __name__ == '__main__':
    schedule = Schedule()
    with open('tournament_team_names.txt',"r") as f:
        for team_name in f:
            l=team_name.split(",")
        for team_name in l :
            schedule.add_team(team_name)

    venues = ['M. A. Chidambaram Stadium, Chennai', 'Wankhede Stadium, Mumbai', 'Eden Gardens, Kolkata', 'Arun Jaitley Stadium, Delhi', 'M. Chinnaswamy Stadium, Bengaluru', 'Sawai Mansingh Stadium, Jaipur', 'Punjab Cricket Association Stadium, Mohali', 'Rajiv Gandhi International Cricket Stadium, Hyderabad']
    for venue in venues:
        schedule.add_venue(venue)

    schedule.generate_schedule()
    schedule.print_schedule('schedule.txt')
