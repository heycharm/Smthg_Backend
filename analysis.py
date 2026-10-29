from datetime import datetime
from collections import defaultdict
import math


def calculate_forecast_accuracy(actuals, forecasts):
    # Group actual 30-minute records by hour
    actual_by_hour = defaultdict(list)

    for record in actuals:
        start_time = record["startTime"]

        # Keep only January 2026
        if not start_time.startswith("2026-01"):
            continue

        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))

        # Example:
        # 23:00 and 23:30 -> 23:00 hour
        hour_key = dt.replace(minute=0, second=0, microsecond=0)

        actual_by_hour[hour_key].append(record["generation"])

    # Calculate hourly actual generation
    hourly_actuals = {}

    for hour, values in actual_by_hour.items():
        hourly_actuals[hour] = sum(values) / len(values)

    # Group forecasts by target hour
    forecasts_by_hour = defaultdict(list)

    for record in forecasts:
        start_time = record["startTime"]

        if not start_time.startswith("2026-01"):
            continue

        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))

        hour_key = dt.replace(minute=0, second=0, microsecond=0)

        forecasts_by_hour[hour_key].append(record)

    results = []

    # Match forecasts with actuals
    for hour, forecast_records in forecasts_by_hour.items():

        actual = hourly_actuals.get(hour)

        if actual is None:
            continue

        for forecast in forecast_records:

            forecast_value = forecast["generation"]

            error = actual - forecast_value

            results.append(
                {
                    "startTime": hour.isoformat(),
                    "publishTime": forecast["publishTime"],
                    "forecast": forecast_value,
                    "actual": actual,
                    "error": error,
                }
            )

    return results


def calculate_metrics(results):
    if not results:
        return {"mae": 0, "rmse": 0, "mape": 0}

    errors = [item["error"] for item in results]

    mae = sum(abs(error) for error in errors) / len(errors)

    rmse = math.sqrt(sum(error**2 for error in errors) / len(errors))

    percentage_errors = []

    for item in results:
        actual = item["actual"]

        if actual != 0:
            percentage_errors.append(abs(item["error"]) / actual * 100)

    mape = sum(percentage_errors) / len(percentage_errors) if percentage_errors else 0

    return {"mae": round(mae, 2), "rmse": round(rmse, 2), "mape": round(mape, 2)}


def get_latest_forecasts(results):
    latest = {}

    for item in results:
        start_time = item["startTime"]

        if (
            start_time not in latest
            or item["publishTime"] > latest[start_time]["publishTime"]
        ):
            latest[start_time] = item

    return list(latest.values())


def calculate_summary(results):
    if not results:
        return {
            "totalHours": 0,
            "averageActual": 0,
            "averageForecast": 0,
            "mae": 0,
            "rmse": 0,
            "mape": 0,
        }

    average_actual = sum(item["actual"] for item in results) / len(results)

    average_forecast = sum(item["forecast"] for item in results) / len(results)

    metrics = calculate_metrics(results)

    return {
        "totalHours": len(results),
        "averageActual": round(average_actual, 2),
        "averageForecast": round(average_forecast, 2),
        "mae": metrics["mae"],
        "rmse": metrics["rmse"],
        "mape": metrics["mape"],
    }


def calculate_daily_data(results):
    daily = defaultdict(list)

    for item in results:
        date = item["startTime"][:10]
        daily[date].append(item)

    output = []

    for date, records in sorted(daily.items()):

        average_actual = sum(item["actual"] for item in records) / len(records)

        average_forecast = sum(item["forecast"] for item in records) / len(records)

        metrics = calculate_metrics(records)

        output.append(
            {
                "date": date,
                "averageActual": round(average_actual, 2),
                "averageForecast": round(average_forecast, 2),
                "mae": metrics["mae"],
                "mape": metrics["mape"],
            }
        )

    return output


