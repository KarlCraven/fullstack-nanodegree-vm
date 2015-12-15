# Tournament.py
Tournament.py is a project built as part of the [Udacity Full Stack Web Developer 
Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
The project uses the [psycopg2 Python module](http://initd.org/psycopg/docs/index.html) 
to interface with a PostgreSQL database. It was built and tested on a virtual 
machine alone.

The project simulates a Swiss-style tournament. More information on Swiss-style 
tournaments can be found on [Wikipedia](https://en.wikipedia.org/wiki/Swiss-system_tournament). 

Two separate versions of the proect are included:

## Versions
### Basic Version
The basic version of this project, located in the main directory, meets the 
minimum requirements of the rubric. It is only set up to run a single tournament 
at a time, and assumes that there are an even number of players to pair up. Only 
match wins are recorded.

### Extra Credit Version
The extra credit version, located in the extra_credit directory, addresses all 
of the project's suggested extra credit criteria, namely:
* Prevent rematches between players.
* Don’t assume an even number of players. If there is an odd number of players, 
assign one player a “bye” (skipped round). A bye counts as a free win. A player 
should not receive more than one bye in a tournament.
* Support games where a draw (tied game) is possible. This will require changing 
the arguments to reportMatch.
* When two players have the same number of wins, rank them according to OMW 
(Opponent Match Wins), the total number of wins by players they have played 
against.
* Support more than one tournament in the database, so matches do not have to 
be deleted between tournaments. This will require distinguishing between “a 
registered player” and “a player who has entered in tournament #123”, so it 
will require changes to the database schema.

## Usage
As far as I am aware, this project will only run within the very specific local 
environment that we were instructed to create for this project, so if you want 
to try it, you will need to:
1 Install [Vagrant](https://www.vagrantup.com/).
2 Install [VirtualBox](https://www.virtualbox.org/).

Once you have everything set up, you will need to:
1 Run Git Bash
2 cd to the 'vagrant' directory.
3 Issue the `vagrant up` command to start up the virtual machine.
4 Log in to the VM with the `vagrant ssh` command.
5 cd within the virtual environment to the '/vagrant/tournament' directory.
6 Import the tournament database using the command `\i tournament.sql`.
7 Connect to the tournament database using the command `\c tournament`.
8 Exit the database environment using the command `\q`.
9 To run the basic functionality tests, run the command `python tournament_test.py`.

Obviously, you will need to adjust the cd commands if you want to test the 
extra credit version. The test file for the extra credit version is
'extra_credit_tests.py'.

## Questions?
Contact me on Twitter @swisodi
