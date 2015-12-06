#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("DELETE FROM matches")
    dbconnection.commit()
    dbconnection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("DELETE FROM players")
    dbconnection.commit()
    dbconnection.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    # Use of 'COALESCE' returns zero instead of 'None' when table is empty
    dbcursor.execute("SELECT COALESCE(COUNT(*), 0) FROM players")
    
    # Assign only the first value in the first tuple to avoid error
    playerCount = dbcursor.fetchall()[0][0]
    
    dbconnection.close()
    return playerCount

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    # Use string insertion method with tuple to prevent SQL injection attacks
    dbcursor.execute("INSERT INTO players (id, name) VALUES (DEFAULT, %s)", (name,))
    
    dbconnection.commit()
    dbconnection.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("SELECT * FROM player_standings")
    
    # Start with an empty list, iterate through results, and append row by row
    playerStandings = []
    for row in dbcursor.fetchall():
        playerStandings.append((row[0], row[1], row[2], row[3]))
    
    dbconnection.close()
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Keeping things orderly by always inserting player IDs lowest to highest
    player1ID = min(winner, loser)
    player2ID = max(winner, loser)
    
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    
    # Use string insertion method with tuple to prevent SQL injection attacks
    dbcursor.execute("INSERT INTO matches (player_1_id, player_2_id, winner_id) VALUES (%s, %s, %s)", (str(player1ID), str(player2ID), str(winner),))
    
    dbconnection.commit()
    dbconnection.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    currentStandings = playerStandings()
    
    # Start with an empty list, iterate through results of playerStandings
    # in pairs and append row by row
    pairList = []
    for i in range(0, len(currentStandings), 2):
        pairList.append((currentStandings[i][0], currentStandings[i][1], currentStandings[i+1][0], currentStandings[i+1][1]))
        
    return pairList