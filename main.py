from teams import Tournament
from match import match
T=Tournament()
T.load_data()
T.generate_teams(2)
t3=T.teams[0]
t4=T.teams[1]
m=match(t3, t4)
m.sim_match(t3, t4)
if __name__ == '__main__':
    T=Tournament()
    T.load_data()
    T.generate_teams(2)
    t3=T.teams[0]
    t4=T.teams[1]
    m=match(t3, t4)
    m.sim_match(t3, t4)
    m.print_scores()