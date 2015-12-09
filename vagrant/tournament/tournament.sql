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


-- Populate players table with demo data
INSERT INTO players (id, name) VALUES
    (DEFAULT, 'Bill'),
    (DEFAULT, 'Bob'),
    (DEFAULT, 'Jim'),
    (DEFAULT, 'Susan'),
    (DEFAULT, 'Anne'),
    (DEFAULT, 'Victoria'),
    (DEFAULT, 'William'),
    (DEFAULT, 'Anneke'),
    (DEFAULT, 'John'),
    (DEFAULT, 'Ian'),
    (DEFAULT, 'Alice'),
    (DEFAULT, 'Jamie'),
    (DEFAULT, 'George'),
    (DEFAULT, 'Sam'),
    (DEFAULT, 'Lee'),
    (DEFAULT, 'Cat');
    

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

-- Populate competitors table with demo data
INSERT INTO competitors (tournament_id, competitor_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (1, 8),
    (2, 9),
    (2, 10),
    (2, 11),
    (2, 12),
    (2, 13),
    (2, 14),
    (2, 15),
    (2, 16);


-- Create matches table    
CREATE TABLE matches (
    tournament_id   integer REFERENCES tournaments(id),
    player_1_id     integer REFERENCES players(id),
    player_2_id     integer REFERENCES players(id),
    winner_id       integer REFERENCES players(id),
    PRIMARY KEY (tournament_id, player_1_id, player_2_id)
);

-- Populate matches table with demo data
--INSERT INTO matches (player_1_id, player_2_id, winner_id) VALUES
--    (1, 2, 1),
--    (3, 4, 3),
--    (5, 6, 6),
--    (7, 8, 7);