# team 1 batting stat
    # for player in m.team1.players :
    #     strike_rate=round(player.batstats.runs/player.batstats.balls_faced*100,2)
    #     cursor.execute("insert into match_{}_bat1(batter,runs,balls,fours,sixes,strike_rate) values({},{},{},{},{},{})".format(id,player.name,player.batstats.runs,player.batstats.balls_faced,player.batstats.num_fours,player.batstats.num_sixes,strike_rate))
    #     connector.commit()
    #     if(player.bowlstats.overs>0):
    #         cursor.execute("insert into match_{}_bowl1(bowler,overs,runs,wickets,economy) values({},{},{},{},{})".format(id,player.name,player.bowlstats.overs,player.bowlstats.runs,player.bowlstats.wickets,player.bowlstats.runs/player.bowlstats.overs))
    #         connector.commit()