# !/usr/bin/env python
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
    dbcursor.execute("INSERT INTO players (id, name) VALUES (DEFAULT, %s)",
                     (name,))

    dbconnection.commit()
    dbconnection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

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
    dbcursor.execute("""INSERT INTO matches (player_1_id, player_2_id,
                        winner_id) VALUES (%s, %s, %s)""",
                     (str(player1ID), str(player2ID), str(winner),))

    dbconnection.commit()
    dbconnection.close()


def havePlayedPreviously(player1, player2):
    """ Returns True if the two players passed as arguments have played each
        other already.

        Queries the matches database looking for the lowest player id as
        player_1_id because we wrote reportMatch() to always sort the player
        ids before creating a new row. This eliminates us having to look for
        the pair in either order in this function."""

    # Assign player ids in a way that'll allow us to search for the lowest
    # first
    player1ID = min(player1, player2)
    player2ID = max(player1, player2)

    # Query the database for this pairing
    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    # Use of 'COALESCE' returns zero instead of 'None' when query returns no
    # rows
    dbcursor.execute(""" SELECT COALESCE(COUNT(*), 0)
                         FROM   matches
                         WHERE  player_1_id = " + str(player1ID) + " AND
                                player_2_id = " + str(player2ID) """)

    # Assign only the first value in the first tuple to avoid error
    previousMatches = dbcursor.fetchall()[0][0]

    dbconnection.close()

    # Return True or False, depending on whether a previous match exists or not
    if (previousMatches > 0):
        return True
    else:
        return False


def swissPairings():
    """ Returns a list of pairs of players for the next round of a match.

        Assuming that there are an even number of players registered, each
        player appears exactly once in the pairings. Each player is paired
        with another player with an equal or nearly-equal win record, that is,
        a player adjacent to him or her in the standings.

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

    # Iterate through each row of the current standings...
    for player in currentStandings:

        # if this player is not in the new pair list...
        if any(player[0] in row for row in pairList) == False:

            # iterate through all of the other players...
            for player2 in currentStandings:

                # and, if the other player is not the same person...
                if player[0] != player2[0]:

                    # if this player is not in the new pair list...
                    if any(player2[0] in row for row in pairList) == False:

                        # check that the other player is not already in the
                        # pairlist and have not already played this player
                        if (havePlayedPreviously(player[0],
                           player2[0]) == False):

                            # .. then add them as the next pair
                            pairList.append((player[0], player[1], player2[0],
                                            player2[1]))
                            break

    return pairList
