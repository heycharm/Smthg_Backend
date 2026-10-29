from elexon import get_wind_actuals, get_wind_forecasts

from analysis import (
    calculate_forecast_accuracy,
    get_latest_forecasts,
    calculate_metrics,
    calculate_summary,
    calculate_daily_data,
)


def get_wind_analysis_data():
    actuals = get_wind_actuals()
    forecasts = get_wind_forecasts()

    results = calculate_forecast_accuracy(actuals, forecasts)

    return get_latest_forecasts(results)


def get_forecast_evolution(forecasts):
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

    return {
        "targetTime": target_hour,
        "data": evolution,
    }
