#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import random

def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    registerPlayer("Victoria Craven")
    registerPlayer("Melva Brown")
    registerPlayer("Jennifer Vincent")
    registerPlayer("Paul Davis")
    print "\n8 players registered."

def testRound():
    matchPairings = swissPairings()
    print "\nPlayers have been paired"
    for row in matchPairings:
        if (random.random() < 0.5):
            print row[1] + " vs. " + row[3] + " -> " + row[1] + " wins!"
            reportMatch(row[0], row[2])
        else:
            print row[1] + " vs. " + row[3] + " -> " + row[3] + " wins!"
            reportMatch(row[2], row[0])
    print "\nMatch winners have been declared. Current standings..."
    currentStandings = playerStandings()
    for row in currentStandings:
        print row[1] + ": " + str(row[2]) + "/" + str(row[3])   

if __name__ == '__main__':
    testRegister()
    print "\nROUND 1! ---------------------------------------------------------"
    testRound()
    print "\nROUND 2! ---------------------------------------------------------"
    testRound()
    print "\nROUND 3! ---------------------------------------------------------"
    testRound()
    print "\n3 rounds have been tested"