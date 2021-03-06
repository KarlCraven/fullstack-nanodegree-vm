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
    dbcursor.execute("DELETE FROM matches;")
    dbconnection.commit()
    dbconnection.close()


def deleteCompetitors():
    """Removes all tournament competitors from the database."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("DELETE FROM competitors;")
    dbconnection.commit()
    dbconnection.close()


def deleteTournaments():
    """Removes all tournaments from the database."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("DELETE FROM tournaments;")
    dbconnection.commit()
    dbconnection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("DELETE FROM players;")
    dbconnection.commit()
    dbconnection.close()


def countCompetitors(tournament_id):
    """Returns the number of competitors currently registered in a specific
    tournament."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    # Use of 'COALESCE' returns zero instead of 'None' when table is empty
    dbcursor.execute("""SELECT COALESCE(COUNT(*), 0)
                        FROM competitors
                        WHERE tournament_id = %s;""",
                     (tournament_id,))

    # Assign only the first value in the first tuple to avoid error
    competitorCount = dbcursor.fetchall()[0][0]

    dbconnection.close()
    return competitorCount


def createTournament(name):
    """Adds a new tournament to the tournaments table."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    # Use string insertion method with tuple to prevent SQL injection attacks
    dbcursor.execute("""INSERT INTO tournaments (id, name) VALUES
                        (DEFAULT, %s);""",
                     (name,))

    dbconnection.commit()
    dbconnection.close()


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
    dbcursor.execute("INSERT INTO players (id, name) VALUES (DEFAULT, %s);",
                     (name,))

    dbconnection.commit()
    dbconnection.close()


def registerCompetitor(tournament_id, competitor_id):
    """ Registers an existing player as a competitor in a specific
        tournament."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    dbcursor.execute("""INSERT INTO competitors (tournament_id, competitor_id,
                        competitor_bye)
                        VALUES (%s, %s, %s);""",
                     (tournament_id, competitor_id, False,))

    dbconnection.commit()
    dbconnection.close()


def useCompetitorBye(tournament_id, competitor_id):
    """Registers that a player's bye has been used in a specific tournament."""
    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    dbcursor.execute("""UPDATE competitors SET competitor_bye = True
                        WHERE tournament_id = %s AND
                              competitor_id = %s""",
                     (tournament_id, competitor_id,))

    dbconnection.commit()
    dbconnection.close()


def playerStandings(tournament_id):
    """ Returns a list of the players and their win records, sorted by wins,
        then draws, then number of matches played, for a specific tournament.

        The first entry in the list should be the player in first place, or a
        player tied for first place if there is currently a tie.

        Returns:
        A list of tuples, each of which contains (id, name, bye, wins,
        matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            bye: whether or not they have used their round bye this tournament
            wins: the number of matches the player has won
            matches: the number of matches the player has played
    """
    dbconnection = connect()
    dbcursor = dbconnection.cursor()
    dbcursor.execute("""SELECT  players.id, players.name,
                                competitors.competitor_bye,
                      (SELECT COUNT(*)
                       FROM   matches
                       WHERE  matches.winner_id = players.id AND
                              tournament_id = %s) as "Wins",
                      (SELECT COUNT(*)
                       FROM   matches
                       WHERE  (matches.player_1_id = players.id OR
                              matches.player_2_id = players.id) AND
                              tournament_id = %s AND
                              matches.draw = True) as "Draws",
                      (SELECT COUNT(*)
                       FROM   matches
                       WHERE  tournament_id = %s AND
                              NOT(matches.winner_id = players.id) AND
                             (matches.winner_id IN (
                              SELECT matches.player_1_id
                              FROM   matches
                              WHERE  matches.player_2_id = players.id AND
                                     tournament_id = %s) OR
                              matches.winner_id IN (
                              SELECT matches.player_2_id
                              FROM   matches
                              WHERE  matches.player_1_id = players.id AND
                                     tournament_id = %s))) as "OMW",
                      (SELECT COUNT(*)
                       FROM   matches
                       WHERE  (matches.player_1_id = players.id OR
                              matches.player_2_id = players.id) AND
                              tournament_id = %s) as "Matches"
                      FROM players INNER JOIN competitors
                           ON (players.id = competitors.competitor_id)
                      WHERE competitors.tournament_id = %s
                      ORDER BY "Wins" DESC, "Draws" DESC, "OMW" DESC,
                               "Matches" DESC;""",
                     (tournament_id, tournament_id, tournament_id,
                      tournament_id, tournament_id, tournament_id,
                      tournament_id,))

    # Start with an empty list, iterate through results, and append row by row
    playerStandings = []
    for row in dbcursor.fetchall():
        playerStandings.append((row[0], row[1], row[2], row[3], row[4], row[5],
                                row[6]))

    dbconnection.close()
    return playerStandings


def reportMatch(tournament_id, player_1_id, player_2_id, winner, draw):
    """Records the outcome of a single match between two players in a specific
    tournament.

    Args:
      tournament_id:  the id of the tournament this match belongs to
      player_1_id: the id of the first player in the match
      player_2_id: the id of the secind player in the match
      winner:  the id number of the player who won (if there was not a draw)
      draw: boolean indicating whether or not the match was a draw
    """
    # Keeping things orderly by always inserting player IDs lowest to highest
    player1ID = min(player_1_id, player_2_id)
    player2ID = max(player_1_id, player_2_id)

    dbconnection = connect()
    dbcursor = dbconnection.cursor()

    # Use string insertion method with tuple to prevent SQL injection attacks
    dbcursor.execute("""INSERT INTO matches (tournament_id, player_1_id,
                        player_2_id, winner_id, draw) VALUES
                        (%s, %s, %s, %s, %s);""",
                     (tournament_id, player1ID, player2ID, winner, draw,))

    dbconnection.commit()
    dbconnection.close()


def havePlayedPreviously(tournament_id, player1, player2):
    """ Returns True if the two players passed as arguments have played each
        other already in this tournament.

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

    # 'COALESCE' returns zero instead of 'None' when query returns no rows
    dbcursor.execute("""SELECT  COALESCE(COUNT(*), 0)
                        FROM    matches
                        WHERE   tournament_id = %s AND
                                player_1_id = %s AND
                                player_2_id = %s;""",
                     (tournament_id, player1ID, player2ID,))

    # Assign only the first value in the first tuple to avoid error
    previousMatches = dbcursor.fetchall()[0][0]

    dbconnection.close()

    # Return True or False, depending on whether a previous match exists or not
    if (previousMatches > 0):
        return True
    else:
        return False


def swissPairings(tournament_id):
    """ Returns a list of pairs of players for the next round of a match in a
        specific tournament.

        Each player is paired with another player with an equal or nearly-equal
        win record (that is, a player adjacent to him or her in the standings).
        If there is an odd number of players, one of them gets a 'bye' for this
        round.

        Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
    """
    currentStandings = playerStandings(tournament_id)

    # If our list of competitors has an odd length...
    if (len(currentStandings) % 2 != 0):

        # ... iterate through the players until we find someone who has not
        # used their round bye in this tournament...
        for player in currentStandings:

            # ... remove them from the list, record in the database that
            # they have now used their bye, and give them a 'win' against
            # themselves
            if (player[2] == False):
                currentStandings.remove(player)
                useCompetitorBye(tournament_id, player[0])
                reportMatch(tournament_id, player[0], player[0], None, False)
                break

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
                        if (havePlayedPreviously(tournament_id, player[0],
                                                 player2[0]) == False):

                            # .. then add them as the next pair
                            pairList.append((player[0], player[1], player2[0],
                                             player2[1]))
                            break

    return pairList
