"""This file contains the SQL table definitions for the database."""

MATCH_DATA_SCHEMA = """
CREATE TABLE IF NOT EXISTS MatchData (
    id SERIAL PRIMARY KEY,
    match_date DATE,
    home_team_name VARCHAR,
    away_team_name VARCHAR,
    home_goals INTEGER,
    away_goals INTEGER,
    home_expected_goals FLOAT,
    away_expected_goals FLOAT,
    goal_difference INTEGER
);
"""

TEAM_SALARIES_SCHEMA = """
CREATE TABLE IF NOT EXISTS TeamSalaries (
    team VARCHAR PRIMARY KEY,
    n INTEGER,
    total_guar DECIMAL,
    avg_guar DECIMAL,
    med_guar DECIMAL,
    std_dev_guar DECIMAL
);
"""

PLAYER_STATS_SCHEMA = """
CREATE TABLE IF NOT EXISTS PlayerStats (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR,
    expected_goals FLOAT,
    expected_assists FLOAT,
    goals_added FLOAT
);
"""