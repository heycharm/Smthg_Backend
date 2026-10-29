from fastapi import FastAPI
from elexon import get_wind_actuals, get_wind_forecasts
from analysis import calculate_forecast_accuracy,calculate_metrics,get_latest_forecasts
from analysis import (
    calculate_forecast_accuracy,
    calculate_metrics,
    get_latest_forecasts,
    calculate_summary,
    calculate_daily_data,
)
from fastapi.middleware.cors import CORSMiddleware
from data_service import get_wind_analysis_data


app = FastAPI(title="Wind Generation Analysis API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Wind Generation Analysis API is running"}


@app.get("/api/wind/actuals")
def wind_actuals():
    return get_wind_actuals()


@app.get("/api/wind/forecasts")
def wind_forecasts():
    return get_wind_forecasts()


@app.get("/api/wind/analysis")
def wind_analysis():

    actuals = get_wind_actuals()
    forecasts = get_wind_forecasts()

    results = calculate_forecast_accuracy(actuals, forecasts)

    latest_results = get_latest_forecasts(results)

    metrics = calculate_metrics(latest_results)

    return {"metrics": metrics, "data": latest_results}


@app.get("/api/wind/summary")
def wind_summary():

    actuals = get_wind_actuals()
    forecasts = get_wind_forecasts()

    results = calculate_forecast_accuracy(actuals, forecasts)

    latest_results = get_latest_forecasts(results)

    return calculate_summary(latest_results)


@app.get("/api/wind/daily")
def wind_daily():

    actuals = get_wind_actuals()
    forecasts = get_wind_forecasts()

    results = calculate_forecast_accuracy(actuals, forecasts)

    latest_results = get_latest_forecasts(results)

    return calculate_daily_data(latest_results)


@app.get("/api/wind/forecast-evolution")
def wind_forecast_evolution():
    forecasts = get_wind_forecasts()

    target_hour = "2026-01-31T23:00:00Z"

    evolution = []

    for forecast in forecasts:
        if forecast["startTime"] == target_hour:
            evolution.append(
                {
                    "publishTime": forecast["publishTime"],
                    "startTime": forecast["startTime"],
                    "forecast": forecast["generation"],
                }
            )

    evolution.sort(key=lambda item: item["publishTime"])

    return {"targetTime": target_hour, "data": evolution}

