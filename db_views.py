"""Database view functions for retrieving player and team statistics."""

import db

def get_top_10_players_with_most_goals_added():
    """Returns the top 10 players with the most goals added."""
    conn = db.get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT player_name, goals_added FROM PlayerStats ORDER BY goals_added DESC LIMIT 10")
    top_10_players = cur.fetchall()
    top_10_players = [{"player_name": row[0], "goals_added": row[1]} for row in top_10_players]
    return top_10_players

def get_rolling_ppg_for_team(team_name):
    """Returns the rolling PPG for a team"""
    conn = db.get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT match_date, home_goals FROM MatchData WHERE home_team_name = %s", (team_name,))
    home_matches = cur.fetchall()
    
    cur.execute("SELECT match_date, away_goals FROM MatchData WHERE away_team_name = %s", (team_name,))
    away_matches = cur.fetchall()
    
    all_matches = home_matches + away_matches
    
    # sort the games by date
    all_matches.sort(key=lambda x: x[0])
    
    matches_count = 0
    points_count = 0
    # data structure {match_date: rolling_ppg}
    rolling_ppg_object = {}
    for match in all_matches:
        matches_count += 1
        points_count += match[1]
        rolling_ppg = round(points_count / matches_count, 3)
        rolling_ppg_object[match[0]] = rolling_ppg
        
    return rolling_ppg_object

def get_total_guaranteed_salaries_for_all_teams():
    """Returns the total guaranteed salaries for all teams"""
    conn = db.get_postgres_connection()
    cur = conn.cursor()
    cur.execute("SELECT team, total_guar FROM TeamSalaries ORDER BY team ASC")
    total_salaries = cur.fetchall()
    total_salaries = [{"team": row[0], "total_guar": row[1]} for row in total_salaries]
    return total_salaries