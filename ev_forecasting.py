import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = "ev_usage_weather.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_FILE, parse_dates=["timestamp"])
df = df.sort_values("timestamp").drop_duplicates()
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.to_period("M").astype(str)
df["weekday"] = df["timestamp"].dt.day_name()
df["date"] = df["timestamp"].dt.date.astype(str)

# Hourly demand summary
hourly = df.groupby("timestamp", as_index=False).agg(
    charging_sessions=("charging_sessions", "sum"),
    temperature_c=("temperature_c", "mean"),
    rain_mm=("rain_mm", "mean"),
    traffic_index=("traffic_index", "mean")
)
hourly.to_csv(os.path.join(OUTPUT_DIR, "tableau_hourly_demand.csv"), index=False)

# Hour and weekday heatmap data
heatmap = df.pivot_table(
    index="weekday", columns="hour",
    values="charging_sessions", aggfunc="mean"
)
weekday_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
heatmap=heatmap.reindex(weekday_order)
heatmap.to_csv(os.path.join(OUTPUT_DIR, "charging_heatmap_data.csv"))

plt.figure(figsize=(12,6))
plt.imshow(heatmap, aspect="auto")
plt.colorbar(label="Average charging sessions")
plt.xticks(range(len(heatmap.columns)), heatmap.columns)
plt.yticks(range(len(heatmap.index)), heatmap.index)
plt.title("Average Charging Demand by Weekday and Hour")
plt.xlabel("Hour of day")
plt.ylabel("Weekday")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "charging_demand_heatmap.png"))
plt.close()

# Daily trend
daily=df.groupby("date", as_index=False)["charging_sessions"].sum()
daily.to_csv(os.path.join(OUTPUT_DIR, "daily_demand.csv"), index=False)
plt.figure(figsize=(12,5))
plt.plot(daily["date"], daily["charging_sessions"])
plt.title("Daily EV Charging Demand")
plt.xlabel("Date")
plt.ylabel("Charging sessions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "daily_demand_trend.png"))
plt.close()

# Baseline forecasting: 7-day seasonal naive model
daily["date"]=pd.to_datetime(daily["date"])
daily=daily.sort_values("date")
daily["forecast_7day_naive"]=daily["charging_sessions"].shift(7)
daily.to_csv(os.path.join(OUTPUT_DIR, "forecast_results.csv"), index=False)

# Forecast next 7 days using average of previous matching weekdays
last_date=daily["date"].max()
future_dates=pd.date_range(last_date+pd.Timedelta(days=1), periods=7, freq="D")
future=[]
for d in future_dates:
    matching=daily[daily["date"].dt.dayofweek==d.dayofweek].tail(4)
    predicted=matching["charging_sessions"].mean() if len(matching) else daily["charging_sessions"].tail(7).mean()
    future.append({"date":d.date().isoformat(),"predicted_sessions":round(float(predicted),2)})
forecast=pd.DataFrame(future)
forecast.to_csv(os.path.join(OUTPUT_DIR, "next_7_days_forecast.csv"),index=False)

# Optimization recommendations
peak_hour=int(df.groupby("hour")["charging_sessions"].mean().idxmax())
low_hour=int(df.groupby("hour")["charging_sessions"].mean().idxmin())
peak_weekday=df.groupby("weekday")["charging_sessions"].mean().idxmax()
recommendations=[
    f"Prioritize charger availability around hour {peak_hour}:00 based on average observed demand.",
    f"Schedule maintenance or non-urgent charging support near hour {low_hour}:00 when demand is lowest.",
    f"Monitor staffing and queue management on {peak_weekday}, which has the highest average demand in this dataset.",
    "Use weather and traffic features in future models to improve forecasting accuracy.",
    "Validate forecasts against real station capacity before operational deployment."
]
with open(os.path.join(OUTPUT_DIR,"charging_optimization_strategy.txt"),"w",encoding="utf-8") as f:
    f.write("Charging Optimization Strategy\n==============================\n\n")
    for r in recommendations:
        f.write("- "+r+"\n")

print("EV charging demand analysis completed.")
print("Open the outputs folder for charts, CSVs, forecasts, and recommendations.")
