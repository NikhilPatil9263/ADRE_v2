# ADRE_v2 — Autonomous Decision & Route Optimization Engine

An intelligent logistics route optimization project designed to evaluate routes using traffic-aware travel information, vehicle parameters, operational costs, emissions and loss-based decision logic.

## Overview

ADRE_v2 aims to improve logistics route planning by combining routing information, traffic and weather conditions, predictive metrics and decision-support mechanisms.

The current implementation focuses on route evaluation and optimization, with a Streamlit dashboard for presenting route metrics and optimization results.

The project is being developed incrementally toward a more comprehensive logistics decision and recovery system.

## Key Features

- **Route Optimization:** Evaluates alternative routes using an operational loss-based optimization approach.
- **Truck Routing:** Integrates TomTom truck-routing capabilities for route information.
- **Traffic Awareness:** Uses traffic information to support route evaluation.
- **Weather Integration:** Incorporates weather conditions into route analysis.
- **ETA Analysis:** Estimates route travel time using available routing and condition data.
- **Fuel Cost Estimation:** Evaluates estimated fuel consumption and cost.
- **Carbon Emission Analysis:** Calculates estimated CO₂ emissions.
- **Decision Support:** Uses an optimization engine to identify the route with the lowest calculated operational loss.
- **Explainability:** Provides explanations for route selection and simulated LLM-style reasoning.
- **Interactive Dashboard:** Displays route comparisons, metrics, charts and explanations through Streamlit.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Routing | TomTom Routing API |
| Traffic Data | Traffic service integration |
| Weather Data | Weather service integration |
| Optimization | Python-based route optimization |
| Data Processing | Pandas, NumPy |
| Explainability | Custom explanation and reasoning modules |
| Version Control | Git and GitHub |

## Project Structure

```text
ADRE_v2/
│
├── cache/
├── config/
│   └── api_keys.py
│
├── dashboard/
│   └── app.py
│
├── data_sources/
│   └── map_service.py
│
├── decision_engine/
│   └── route_optimizer.py
│
├── digital_twin/
│   ├── loss_engine.py
│   ├── route_model.py
│   ├── twin_state.py
│   ├── updater.py
│   └── vehicle_model.py
│
├── event_ingestion/
│
├── explainability/
│   ├── explanation_engine.py
│   ├── llm_reasoner.py
│   ├── prompts.py
│   └── templates.py
│
├── predictive_engine/
│   ├── carbon_predictor.py
│   ├── eta_predictor.py
│   ├── fuel_predictor.py
│   ├── risk_predictor.py
│   └── metrics_bundle.py
│
├── services/
│   ├── city_registry.py
│   ├── live_routing.py
│   ├── map_services.py
│   ├── traffic_service.py
│   └── weather_service.py
│
├── run_phase3.py
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/NikhilPatil9263/ADRE_v2.git
```

### 2. Navigate to the project

```bash
cd ADRE_v2
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies specified by your project's imports.

### 5. Configure API keys

The project reads API keys through environment variables.

Set them in PowerShell:

```powershell
$env:TOMTOM_API_KEY="YOUR_TOMTOM_API_KEY"
$env:OPENWEATHER_API_KEY="YOUR_OPENWEATHER_API_KEY"
```

Replace the placeholders with your own API keys.

**Security:** Never commit API keys, credentials or `.env` files to GitHub.

## Running the Project

### Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

Open the local dashboard:

```text
http://localhost:8501
```

### Run the Phase 3 pipeline

```bash
python run_phase3.py
```

## Dashboard

The current dashboard provides:

- Route optimization execution
- Route comparison results
- Estimated arrival time analysis
- Total operational loss visualization
- CO₂ emission visualization
- AI-based explanation and simulated reasoning output

## Current Implementation Status

| Component | Status |
|---|---|
| Route evaluation | Implemented |
| Route optimization engine | Implemented |
| Digital Twin components | Implemented |
| ETA, fuel and emission calculations | Implemented |
| Traffic and weather integration | Implemented |
| TomTom truck-routing test | Successfully tested |
| Streamlit dashboard | Implemented |
| Explainability module | Implemented |
| Live LLM integration | Not yet implemented |
| Advanced disruption recovery workflow | Planned |
| Human approval and recovery execution | Planned |

*The project is under active development. Implementation status may change as additional modules are integrated and tested.*

## Future Development

The planned development direction includes:

- Real-time logistics disruption detection.
- LangGraph-based decision workflows.
- Retrieval-Augmented Generation (RAG) for logistics policies.
- Vector database integration.
- Alternative vehicle and route recovery recommendations.
- Human-in-the-loop approval.
- Backend API integration.
- Real-time dashboard updates.
- Docker-based application setup.

These are development goals and should not be interpreted as completed features.

## Project Objective

The long-term objective of ADRE_v2 is to move beyond conventional route optimization toward an intelligent logistics decision-support system capable of analyzing operational disruptions and recommending suitable recovery actions.

## Author

**Nikhil Patil**

GitHub: [NikhilPatil9263](https://github.com/NikhilPatil9263)

**Repository:** [ADRE_v2](https://github.com/NikhilPatil9263/ADRE_v2)

---

*ADRE_v2 — Intelligent Route Optimization and Logistics Decision Support.*
