# Electric Vehicle Charging Demand Forecasting

## Objective
Forecast and analyze EV charging demand based on time, weather, and traffic indicators.

## Tools
- Python
- Pandas
- NumPy
- Matplotlib
- Excel
- Tableau

## Important note
The included dataset is synthetic demonstration data. It is not actual EV station data and must not be presented as measured real-world demand.

## Run
```bash
pip install -r requirements.txt
python ev_forecasting.py
```

## Deliverables
- charging_demand_heatmap.png
- daily_demand_trend.png
- charging_heatmap_data.csv
- tableau_hourly_demand.csv
- daily_demand.csv
- forecast_results.csv
- next_7_days_forecast.csv
- charging_optimization_strategy.txt

## Excel
Open the CSV files in Excel and create:
1. PivotTable: average sessions by weekday and hour
2. Line chart: daily demand
3. Conditional-formatting heatmap
4. Forecast comparison table

## Tableau dashboard suggestions
- KPI: total charging sessions
- Line chart: demand over time
- Heatmap: weekday versus hour
- Filters: station, weekday, month
- Forecast table: next 7 days

## Forecasting note
This starter project includes a seasonal-naive baseline forecast using the previous matching weekday. For an advanced submission, compare this baseline with ARIMA, Prophet, or a regression model using weather and traffic variables. Report MAE/RMSE on a held-out test period.
