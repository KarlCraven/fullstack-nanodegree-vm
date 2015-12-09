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
               "Mandy Myrtle", "Ned Nelson", "Oliver Ort", "Pat Pearson"]
    for player in players:
        registerPlayer(player)
    print "\n" + str(len(players)) + " players registered."


def testCreateTournament():
    createTournament("Test Tournament")
    print "\nTest tournament created"

    
def testRegisterCompetitors():
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    dbcursor.execute("SELECT id FROM players;")
    player_ids = []
    for row in dbcursor.fetchall():
        player_ids.append(row)
    
    dbcursor.execute("SELECT id FROM tournaments;")
    tournament_ids = []
    for row in dbcursor.fetchall():
        tournament_ids.append(row)
    t_id = tournament_ids[0][0]
    
    dbconnection.commit()
    dbconnection.close()
    
    for id in player_ids:
        registerCompetitor(t_id, id)
    
    print "\n" + str(len(player_ids)) + " competitors registered."
    
    return t_id
    
    
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
        print row[1] + ": " + str(row[2]) + "/" + str(row[3])   

if __name__ == '__main__':
    clearAllTables()
    testRegisterPlayers()
    testCreateTournament()
    tournament_id = testRegisterCompetitors()
    print(tournament_id)
    print "\nROUND 1! ---------------------------------------------------------"
    testPlayRounds(tournament_id)
    print "\nROUND 2! ---------------------------------------------------------"
    testPlayRounds(tournament_id)
    print "\nROUND 3! ---------------------------------------------------------"
    testPlayRounds(tournament_id)
    print "\n3 rounds have been tested"