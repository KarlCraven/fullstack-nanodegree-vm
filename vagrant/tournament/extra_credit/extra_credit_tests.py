#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import random

def clearAllTables():
    """Empties all tables in the database."""
    deleteMatches()
    deleteCompetitors()
    deleteTournaments()
    deletePlayers()
    print "All tables emptied"


def testRegisterPlayers():
    """Registers 17 players in the database."""
    players = ["Adam Abrams", "Bob Buick", "Cecil Christian", "David Dallas",
               "Esther Evans", "Francis Farrow", "Gillian Graham", "Hal Hart",
               "Ian Isthmus", "Jennifer Jones", "Karen Kit", "Lorna Levi",
               "Mandy Myrtle", "Ned Nelson", "Oliver Ort", "Pat Pearson",
               "Quincy Quatermass"]
    for player in players:
        registerPlayer(player)
    print "\n" + str(len(players)) + " players registered."


def testCreateTournament():
    """Creates two tournaments in the database."""
    createTournament("Tournament 1")
    createTournament("Tournament 2")
    print "\nTest tournaments created"

    
def testRegisterCompetitors():
    """Registers our players aternately into one of the two tournaments."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    # get all our registered player ids and split them into two arrays
    dbcursor.execute("SELECT id FROM players;")
    t1_player_ids = []
    t2_player_ids = []
    i = 0
    
    for row in dbcursor.fetchall():
        if (i % 2 == 0):
            t1_player_ids.append(row)
        else:
            t2_player_ids.append(row)
        i+=1
    
    # get both of our current tournament ids and assign them to variables we can
    # pass on to additional test functions
    dbcursor.execute("SELECT id FROM tournaments;")
    tournament_ids = []
    
    for row in dbcursor.fetchall():
        tournament_ids.append(row)
    
    t_id_1 = tournament_ids[0][0]
    t_id_2 = tournament_ids[1][0]
    
    dbconnection.commit()
    dbconnection.close()
    
    # register players as competitors in tournaments
    for id1 in t1_player_ids:
        registerCompetitor(t_id_1, id1)
    
    for id2 in t2_player_ids:
        registerCompetitor(t_id_2, id2)
    
    print "\n" + str(len(t1_player_ids)) + \
          " competitors registered in tournament " + str(t_id_1)
    print "\n" + str(len(t2_player_ids)) + \
          " competitors registered in tournament " + str(t_id_2)
    
    # combine tournament ids into a tuple we can return
    t_id_tuple = (t_id_1, t_id_2)
    return t_id_tuple
    
    
def testPlayRounds(t_id):
    """Simulates three rounds of the tournament, outputting match outcomes
       and player standings tables for each round."""
    matchPairings = swissPairings(t_id)
    print "\nPlayers have been paired...\n"
    
    # Use random numbers to decide the outcomes of each match in this tournament
    # and outputs the results
    for row in matchPairings:
        randomNum = random.random()
        if (randomNum < 0.33):
            print row[1] + " vs. " + row[3] + " -> " + row[1] + " wins!"
            reportMatch(t_id, row[0], row[2], row[0], False)
        elif (randomNum < 0.66):
            print row[1] + " vs. " + row[3] + " -> " + row[3] + " wins!"
            reportMatch(t_id, row[0], row[2], row[2], False)
        else:
            print row[1] + " vs. " + row[3] + " -> draw!"
            reportMatch(t_id, row[2], row[0], None, True)
    
    # Output a table of the current player standings for this tournament
    print "\nMatch winners have been declared. Current standings..."
    print "\nPlayer Name       |  Wins   |  Draws  | O.M.W.  | Matches |" + \
          " Bye Used?"
    print "--------------------------------------------------------------------"
    currentStandings = playerStandings(t_id)
    for row in currentStandings:
        spacing = ""
        
        # This just helps us keep the table aligned for easy browsing regardless
        # of the length of the player's name
        for space in range(18-len(row[1])):
            spacing += " "
        
        print row[1] + spacing + "|    " + str(row[3]) + "    |    " + \
              str(row[4]) + "    |    " + str(row[5]) + "    |    " + \
              str(row[6]) + "    | " + str(row[2])
    print "--------------------------------------------------------------------"
    

if __name__ == '__main__':
    """Calls all of our test functions above."""
    clearAllTables()
    testRegisterPlayers()
    testCreateTournament()
    tournament_id = testRegisterCompetitors()
    
    # Simulate tournament rounds, with friendly output for easier reading.
    for id in tournament_id:
        print "\n"
        print "\n=============================================================="
        print "\nBeginning Tournament " + str(id) + "..."
        print "\n=============================================================="
        print "\nROUND 1! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        testPlayRounds(id)
        print "\nROUND 2! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        testPlayRounds(id)
        print "\nROUND 3! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        testPlayRounds(id)
        print "\n3 rounds have been tested"