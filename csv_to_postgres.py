"""
Module for ingesting MLS (Major League Soccer) data from CSV files into PostgreSQL database.

This module provides functions to load and transform data from CSV files containing:
- Match data (scores, expected goals)
- Team salary information
- Player statistics (expected goals, assists, and goals added)

Each function handles data cleaning, transformation, and insertion into corresponding
PostgreSQL database tables.
"""
import pandas as pd
from psycopg2 import Error
from schemas import MATCH_DATA_SCHEMA, TEAM_SALARIES_SCHEMA, PLAYER_STATS_SCHEMA
import db

def check_table_has_data(cur, table_name):
    """Check if the specified table already has data"""
    cur.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} LIMIT 1)")
    return cur.fetchone()[0]

def data_ingestion_matches():
    """Ingests match data from CSV files into PostgreSQL database"""
    # good to know - Each Major League Soccer (MLS) team plays 34 games in the regular season.
    conn = None
    cur = None
    try:
        conn = db.get_postgres_connection()
        cur = conn.cursor()
        cur.execute(MATCH_DATA_SCHEMA)
        conn.commit()

        # Check if data already exists
        if check_table_has_data(cur, 'MatchData'):
            print("MatchData table already contains data. Skipping ingestion.")
            return

        df = pd.read_csv("data/csv_files/xGoals/games.csv")
        
        df_columns = {
            'Date': 'match_date',  
            'Home': 'home_team_name',  
            'Away': 'away_team_name',  
            'HG': 'home_goals',    
            'AG': 'away_goals',    
            'HxGt': 'home_expected_goals',  
            'AxGt': 'away_expected_goals',
            'GD': 'goal_difference'
        }

        df = df.rename(columns=df_columns)
        
        columns = ['match_date', 'home_team_name', 'away_team_name', 'home_goals', 
                'away_goals', 'home_expected_goals', 'away_expected_goals', 'goal_difference']

        inserted_count = 0
        for _,row in df.iterrows():
            # if we get NaN, make it 0
            for col in columns:
                if pd.isna(row[col]):
                    row[col] = 0
                    
            insert_query = f"""
                INSERT INTO MatchData ({', '.join(columns)}) 
                VALUES ({', '.join(['%s'] * len(columns))});
            """
            values = [row[col] for col in columns]
            cur.execute(insert_query, values)
            inserted_count += 1

        conn.commit()
        print(f"Successfully inserted {inserted_count} matches into MatchData")

    except FileNotFoundError as e:
        print(f"CSV file not found: {e}")
        raise
    except pd.errors.EmptyDataError:
        print("The CSV file is empty")
        raise
    except Error as db_error:
        print(f"Database error occurred: {db_error}")
        raise
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
def data_ingestion_team_salaries():
    """Ingests team salaries for the 2024 MLS season"""
    conn = None
    cur = None
    try:
        conn = db.get_postgres_connection()
        cur = conn.cursor()
        cur.execute(TEAM_SALARIES_SCHEMA)
        conn.commit()

        if check_table_has_data(cur, 'TeamSalaries'):
            print("TeamSalaries table already contains data. Skipping ingestion.")
            return

        df = pd.read_csv("data/csv_files/Salaries/teams.csv")
        
        df_columns = {
            'Team': 'team',
            'N': 'n',
            'TotalGuar': 'total_guar',
            'AvgGuar': 'avg_guar',
            'MedGuar': 'med_guar',
            'StdDevGuar': 'std_dev_guar'
        }
        
        df = df.rename(columns=df_columns)
        
        # Drop any unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Skip rows where team is null or empty
        df = df[df['team'].notna() & (df['team'] != '')]
        
        # Clean monetary values by removing '$' and ',' before converting to float
        monetary_columns = ['total_guar', 'avg_guar', 'med_guar', 'std_dev_guar']
        for col in monetary_columns:
            df[col] = df[col].str.replace('$', '').str.replace(',', '').astype(float)
        
        inserted_count = 0
        for _, row in df.iterrows():
            insert_query = f"""
                INSERT INTO TeamSalaries ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))});
            """
            values = [row[col] for col in df.columns]
            cur.execute(insert_query, values)
            inserted_count += 1
        
        conn.commit()
        print(f"Successfully inserted {inserted_count} team salary records into TeamSalaries")
        
    except Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        

def data_ingestion_player_stats():
    """Ingests player statistics including expected goals, expected assists, and goals added"""
    conn = None
    cur = None
    try:
        conn = db.get_postgres_connection()
        cur = conn.cursor()
        cur.execute(PLAYER_STATS_SCHEMA)
        conn.commit()

        if check_table_has_data(cur, 'PlayerStats'):
            print("PlayerStats table already contains data. Skipping ingestion.")
            return

        goals_added_df = pd.read_csv("data/csv_files/g+/players.csv")
        xgoals_df = pd.read_csv("data/csv_files/xGoals/players.csv")

        goals_added_df.drop_duplicates(subset=['Player'], keep='first', inplace=True)
        xgoals_df.drop_duplicates(subset=['Player'], keep='first', inplace=True)

        player_stats_df_columns = {
            'Player': 'player_name',
            'xG': 'expected_goals',
            'xA': 'expected_assists',
            'Goals Added': 'goals_added'
        }

        goals_added_df = goals_added_df[['Player', 'Goals Added']]
        xgoals_df = xgoals_df[['Player', 'xG', 'xA']] 
        
        player_stats_df = goals_added_df.merge(xgoals_df, on='Player', how='outer')

        player_stats_df = player_stats_df.rename(columns=player_stats_df_columns)

        columns_to_insert = ['player_name', 'expected_goals', 'expected_assists', 'goals_added']
    
        inserted_count = 0
        for _, row in player_stats_df.iterrows():
            # if we get NaN, lets make it 0
            for col in columns_to_insert:
                if pd.isna(row[col]):
                    row[col] = 0
                    
            insert_query = f"""
                INSERT INTO PlayerStats ({', '.join(columns_to_insert)}) 
                VALUES ({', '.join(['%s'] * len(columns_to_insert))});
            """
            values = [row[col] for col in columns_to_insert]
            cur.execute(insert_query, values)
            inserted_count += 1
            
        conn.commit()
        print(f"Successfully inserted {inserted_count} player statistics records into PlayerStats")

    except Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
