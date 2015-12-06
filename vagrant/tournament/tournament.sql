-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW IF EXISTS player_standings;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS tournament;

CREATE DATABASE tournament;

CREATE TABLE players (
	id		serial PRIMARY KEY,
	name	text
);

INSERT INTO players (id, name) VALUES
	(DEFAULT, 'Bill'),
	(DEFAULT, 'Bob'),
	(DEFAULT, 'Jim'),
	(DEFAULT, 'Susan'),
	(DEFAULT, 'Anne'),
	(DEFAULT, 'Victoria');

 
CREATE TABLE matches (
	player_1_id	integer REFERENCES players(id),
	player_2_id	integer REFERENCES players(id),
	winner_id	integer REFERENCES players(id),
	PRIMARY KEY (player_1_id, player_2_id)
);

INSERT INTO matches (player_1_id, player_2_id, winner_id) VALUES
	(1, 2, 1),
	(3, 4, 3),
	(5, 6, 6);

CREATE VIEW player_standings AS
	SELECT	players.id, players.name, 
	(SELECT	COUNT(*)
	 FROM	matches
	 WHERE	matches.winner_id = players.id) as "Wins",
	(SELECT	COUNT(*)
	 FROM	matches
	 WHERE	matches.player_1_id = players.id OR
			matches.player_2_id = players.id) as "Matches"
	FROM players
	ORDER BY "Wins" DESC, "Matches" DESC
