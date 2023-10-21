"""
This is a work in progress
"""

import pandas as pd
from ydata_profiling import ProfileReport

FILE_PATH = "./data/raw/hockey_teams_raw.csv"

# Import & perform necessary transformation in the dataframe
hockey_df = (
    pd.read_csv(FILE_PATH, index_col=False)
    .pipe(lambda x: x.drop(columns=["scrape_timestamp", "goals_diff"]))
    .pipe(lambda x: x.fillna(0) if "ot_losses" in x.columns else x)
    .pipe(lambda x: x.astype({"ot_losses": int, "year": str}))
)

# Generate Automated EDA Report with ydata Profiling library
profile = ProfileReport(hockey_df, explorative=True,
                        title="Hockey Team Stats - Data Profile Report")
profile.to_file("./reports/data_profiling_report.html")

# Export clean data
OUTPUT_FILE_PATH = "./data/processed/hockey_team_stats.csv"
hockey_df.to_csv(OUTPUT_FILE_PATH, index=False)
