#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import random

def clearAllTables():
    deleteMatches()
    deleteCompetitors()
    deleteTournaments()
    deletePlayers()
    print "All tables emptied"


def testRegisterPlayers():
    players = ["Adam Abrams", "Bob Buick", "Cecil Christian", "David Dallas",
               "Esther Evans", "Francis Farrow", "Gillian Graham", "Hal Hart",
               "Ian Isthmus", "Jennifer Jones", "Karen Kit", "Lorna Levi",
               "Mandy Myrtle", "Ned Nelson", "Oliver Ort", "Pat Pearson",
               "Quincy Quatermass"]
    for player in players:
        registerPlayer(player)
    print "\n" + str(len(players)) + " players registered."


def testCreateTournament():
    createTournament("Tournament 1")
    createTournament("Tournament 2")
    print "\nTest tournaments created"

    
def testRegisterCompetitors():
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    dbcursor.execute("SELECT id FROM players;")
    t1_player_ids = []
    t2_player_ids = []
    i = 0
    
    for row in dbcursor.fetchall():
        print str(i)
        if (i % 2 == 0):
            t1_player_ids.append(row)
        else:
            t2_player_ids.append(row)
        i+=1
    
    dbcursor.execute("SELECT id FROM tournaments;")
    tournament_ids = []
    
    for row in dbcursor.fetchall():
        tournament_ids.append(row)
    
    t_id_1 = tournament_ids[0][0]
    t_id_2 = tournament_ids[1][0]
    
    dbconnection.commit()
    dbconnection.close()
    
    for id1 in t1_player_ids:
        registerCompetitor(t_id_1, id1)
    
    for id2 in t2_player_ids:
        registerCompetitor(t_id_2, id2)
    
    print "\n" + str(len(t1_player_ids)) + \
          " competitors registered in tournament " + str(t_id_1)
    print "\n" + str(len(t2_player_ids)) + \
          " competitors registered in tournament " + str(t_id_2)
    
    t_id_tuple = (t_id_1, t_id_2)
    return t_id_tuple
    
    
def testPlayRounds(t_id):
    matchPairings = swissPairings(t_id)
    print "\nPlayers have been paired"
    for row in matchPairings:
        if (random.random() < 0.5):
            print row[1] + " vs. " + row[3] + " -> " + row[1] + " wins!"
            reportMatch(t_id, row[0], row[2])
        else:
            print row[1] + " vs. " + row[3] + " -> " + row[3] + " wins!"
            reportMatch(t_id, row[2], row[0])
    print "\nMatch winners have been declared. Current standings..."
    currentStandings = playerStandings(t_id)
    for row in currentStandings:
        print row[1] + ": " + str(row[3]) + "/" + str(row[4]) + " (" + \
              str(row[2]) + ")"  

if __name__ == '__main__':
    clearAllTables()
    testRegisterPlayers()
    testCreateTournament()
    tournament_id = testRegisterCompetitors()
    
    for id in tournament_id:
        print "\n=============================================================="
        print "\nBeginning Tournament " + str(id) + "..."
        print "\n"
        print "\nROUND 1! -----------------------------------------------------"
        testPlayRounds(id)
        print "\nROUND 2! -----------------------------------------------------"
        testPlayRounds(id)
        print "\nROUND 3! -----------------------------------------------------"
        testPlayRounds(id)
        print "\n3 rounds have been tested"