	
import pandas as pd

# load dataset
df = pd.read_csv("backend/data/resume_cleaned.csv")

# print all unique job roles
print(df["job_position_name"].unique())