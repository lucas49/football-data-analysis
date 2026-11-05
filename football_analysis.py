
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# 1. Load and Explore Match Data
# ==========================================

url = "https://www.football-data.co.uk/mmz4281/2526/E0.csv"
df = pd.read_csv(url)

print("Dataset dimensions:", df.shape)

print("\nFirst five matches:")
print(df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].head())

print("\nMissing values in key columns:")
print(df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].isna().sum())


# ==========================================
# 2. Analyze Match Results
# ==========================================

result_counts = df["FTR"].value_counts().reindex(["H", "D", "A"], fill_value=0)
result_percentages = (result_counts / len(df)) * 100

result_summary = pd.DataFrame({
    "Matches": result_counts,
    "Percentage": result_percentages.round(2)
})

print("\nMatch Results Summary:")
print(result_summary)


# ==========================================
# 3. Analyze Total Goals
# ==========================================

total_goals_per_match = df["FTHG"] + df["FTAG"]

total_goals = total_goals_per_match.sum()
total_matches = len(df)
overall_average_goals = total_goals_per_match.mean()
median_goals = total_goals_per_match.median()

print("\nGoal Analysis:")
print("Total goals:", total_goals)
print("Total matches:", total_matches)
print("Average goals per match:", round(overall_average_goals, 2))
print("Median goals per match:", median_goals)


# ==========================================
# 4. Compare Home and Away Goals
# ==========================================

home_goals = df["FTHG"].sum()
away_goals = df["FTAG"].sum()

home_goals_avg = df["FTHG"].mean()
away_goals_avg = df["FTAG"].mean()

print("\nHome vs Away Goals:")
print("Total home goals:", home_goals)
print("Total away goals:", away_goals)
print("Average home goals per match:", round(home_goals_avg, 2))
print("Average away goals per match:", round(away_goals_avg, 2))


# ==========================================
# 5. Analyze Drawn Matches
# ==========================================

draw_matches = df[df["FTR"] == "D"]
draw_goals = draw_matches["FTHG"] + draw_matches["FTAG"]

average_draw_goals = draw_goals.mean()

print("\nDraw Match Analysis:")
print("Number of drawn matches:", len(draw_matches))
print("Average goals in drawn matches:", round(average_draw_goals, 2))


# ==========================================
# 6. Analyze Goals by Match Result
# ==========================================

home_wins = df[df["FTR"] == "H"]
away_wins = df[df["FTR"] == "A"]

home_win_goals = home_wins["FTHG"] + home_wins["FTAG"]
away_win_goals = away_wins["FTHG"] + away_wins["FTAG"]

print("\nGoals by Match Result:")
print("Home wins:", len(home_wins),
      "| Average goals:", round(home_win_goals.mean(), 2))
print("Draws:", len(draw_matches),
      "| Average goals:", round(draw_goals.mean(), 2))
print("Away wins:", len(away_wins),
      "| Average goals:", round(away_win_goals.mean(), 2))


# ==========================================
# 7. Analyze Goal Distribution
# ==========================================

goal_distribution = total_goals_per_match.value_counts().sort_index()
goal_percentages = (goal_distribution / total_matches) * 100

goal_summary = pd.DataFrame({
    "Matches": goal_distribution,
    "Percentage": goal_percentages.round(2)
})

print("\nGoal Distribution Summary:")
print(goal_summary)

goal_summary.to_csv(
    "goal_distribution_summary.csv",
    index_label="Goals"
)

print("\nGoal summary exported successfully.")


# ==========================================
# 8. Prepare Output Folder
# ==========================================

output_folder = Path("images")
output_folder.mkdir(exist_ok=True)


# ==========================================
# 9. Visualize Goal Distribution
# ==========================================

plt.figure(figsize=(9, 5))
plt.bar(goal_distribution.index, goal_distribution.values)

for goals, matches in zip(goal_distribution.index, goal_distribution.values):
    plt.text(goals, matches, str(matches), ha="center", va="bottom")

plt.title("Distribution of Goals per Match")
plt.xlabel("Total Goals in Match")
plt.ylabel("Number of Matches")
plt.xticks(goal_distribution.index)
plt.ylim(0, max(goal_distribution.values) + 15)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

plt.savefig(output_folder / "goal_distribution.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# 10. Visualize Average Goals: Home vs Away
# ==========================================

location_averages = [home_goals_avg, away_goals_avg]
teams = ["Home Teams", "Away Teams"]

plt.figure(figsize=(8, 5))
plt.bar(teams, location_averages)

for team, goals in zip(teams, location_averages):
    plt.text(team, goals, f"{goals:.2f}", ha="center", va="bottom")

plt.title("Average Goals: Home vs Away")
plt.xlabel("Team Location")
plt.ylabel("Average Goals per Match")
plt.ylim(0, 2)
plt.tight_layout()

plt.savefig(output_folder / "average_goals_comparison.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# 11. Visualize Match Results
# ==========================================

result_labels = ["Home Wins", "Draws", "Away Wins"]

plt.figure(figsize=(8, 5))
plt.bar(result_labels, result_counts.values)

for label, count in zip(result_labels, result_counts.values):
    plt.text(label, count, str(count), ha="center", va="bottom")

plt.title("Distribution of Match Results")
plt.xlabel("Match Result")
plt.ylabel("Number of Matches")
plt.ylim(0, max(result_counts.values) + 20)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

plt.savefig(output_folder / "match_results.png", dpi=300)
plt.show()
plt.close()

print("\nAll charts exported successfully.")
