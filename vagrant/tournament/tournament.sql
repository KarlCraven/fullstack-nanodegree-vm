-- Database schema for the tournament project.

-- Drop all existing tables and views
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS competitors CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments;


-- Create players table
CREATE TABLE players (
    id      serial PRIMARY KEY,
    name    text
);
    

-- Create tournaments table 
CREATE TABLE tournaments (
    id      serial PRIMARY KEY,
    name    text
);


-- Populate tournaments table with demo data
INSERT INTO tournaments (id, name) VALUES
    (DEFAULT, '2014 Grand Slam'),
    (DEFAULT, '2015 Charity Cup');


-- Create tournament competitors table
CREATE TABLE competitors (
    tournament_id   integer REFERENCES tournaments(id),
    competitor_id   integer REFERENCES players(id),
    PRIMARY KEY (tournament_id, competitor_id)
);


-- Create matches table    
CREATE TABLE matches (
    tournament_id   integer REFERENCES tournaments(id),
    player_1_id     integer REFERENCES players(id),
    player_2_id     integer REFERENCES players(id),
    winner_id       integer REFERENCES players(id),
    PRIMARY KEY (tournament_id, player_1_id, player_2_id)
);