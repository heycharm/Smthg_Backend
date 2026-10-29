# Wind Generation Analysis — Backend

Python backend for analysing UK national-level wind generation actuals and forecasts using data from the **Elexon BMRS API**.

The backend focuses on **January 2026** and provides APIs for comparing wind generation forecasts with actual generation and measuring forecast accuracy.

## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- Requests
- Docker

## Data Source

All energy data is retrieved from the **Elexon BMRS API**.

### Actual Generation

Dataset: `FUELHH`

Fuel type: `WIND`

The actual generation data is available at 30-minute intervals. The backend aggregates the two half-hour values into an hourly actual generation value for comparison with the hourly forecast data.

### Wind Forecasts

Dataset: `WINDFOR`

The forecast data contains:

- `startTime` — target generation time
- `publishTime` — forecast publication time
- `generation` — forecast wind generation

Multiple forecasts can exist for the same target hour. The latest forecast is selected using the latest `publishTime`.

## Project Structure

```text
GridBlocksAssignment_Backend/
├── main.py
├── elexon.py
├── analysis.py
├── data_service.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

### Files

**`main.py`**

Defines the FastAPI application and API routes.

**`elexon.py`**

Handles requests to the Elexon BMRS API.

**`analysis.py`**

Contains the forecast comparison and accuracy calculations, including:

- Latest forecast selection
- Forecast error
- MAE
- RMSE
- MAPE
- Daily accuracy calculations

**`data_service.py`**

Coordinates data retrieval and analysis for the API endpoints.

**`requirements.txt`**

Contains the Python dependencies required by the backend.

**`Dockerfile`**

Defines the Docker image used to run the backend.

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/wind/actuals` | Wind actual generation |
| `/api/wind/forecasts` | Wind forecast data |
| `/api/wind/analysis` | Actual vs forecast analysis |
| `/api/wind/summary` | Overall accuracy summary |
| `/api/wind/daily` | Daily accuracy data |
| `/api/wind/forecast-evolution` | Forecast evolution for a target period |

Interactive API documentation is available through FastAPI:

```text
/docs
```

## Analysis Approach

The backend follows these steps:

1. Retrieve January 2026 wind actual generation from Elexon.
2. Retrieve January 2026 wind forecast data.
3. Aggregate the 30-minute actual values into hourly values.
4. Match actual generation with forecast target hours.
5. Select the latest available forecast for each target hour using `publishTime`.
6. Calculate forecast error.

```text
Error = Actual Generation - Forecast Generation
```

7. Calculate forecast accuracy metrics.
8. Return the processed data through the API.

## Accuracy Metrics

### MAE

Mean Absolute Error measures the average absolute difference between forecast and actual generation.

### RMSE

Root Mean Squared Error gives greater weight to larger forecast errors.

### MAPE

Mean Absolute Percentage Error expresses forecast error relative to actual generation.

## Running Locally

### Prerequisites

- Python 3.12+
- pip

Clone the repository and navigate to the backend directory:

```bash
cd Smthg_Backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
python -m uvicorn main:app --reload
```

<!-- The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
``` -->

## Running with Docker

Build the image:

```bash
docker build -t wind