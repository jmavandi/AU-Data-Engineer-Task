# Atlanta United FC Data Analysis Take-Home

### Prerequisites

- Docker
- Docker Compose

## Installation & Setup

1. Clone this repository
2. Navigate to the project directory
3. Run `docker compose up`
4. Wait for the Jupyter server to start
5. Open [http://127.0.0.1:8888/lab/tree/notebooks.ipynb](http://127.0.0.1:8888/lab/tree/notebooks.ipynb) in your browser

## Using the Notebook

1. Once opened, click the "Run All" button (») in the toolbar
2. Scroll down to view the generated visualizations:
   - Top 10 Players with the Most Goals Added (g+)
   - Atlanta United FC Rolling Points Per Game Over The Season
   - All 2024 MLS Teams Guaranteed Salaries Compared

## Technical Implementation

This project implements a data analysis pipeline with the following components and rationale:

1. **Data Collection**:

   - Sourced official MLS match and player statistics data
   - Data manually exported as CSVs to ensure data integrity and version control

2. **Database**:

   - PostgreSQL was chosen as the database solution for:
     - Robust support for complex SQL queries
     - Strong data integrity constraints
     - Excellent performance with analytical workloads
     - Native support for JSON data types

3. **Data Processing**:

   - Python scripts handle:
     - Database table creation and schema management
     - CSV data parsing and database population
     - Data validation and transformation

4. **Analysis Layer**:

   - Custom Python functions wrap SQL queries for:
     - Data aggregation and statistical calculations
     - Performance metrics computation
     - Time-series analysis

5. **Visualization**:

   - Jupyter Notebook was selected because it:
     - Provides interactive data exploration
     - Supports rich visualization libraries (matplotlib, seaborn)
     - Allows code and documentation to coexist
     - Makes analysis steps transparent and reproducible

6. **Deployment**:
   - Docker Compose orchestrates:
     - PostgreSQL database container
     - Jupyter Notebook server
   - Containerization ensures consistent environment across different systems
   - Zero-configuration setup for end users
