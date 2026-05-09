# Human Body Measurement Explorer

An interactive web dashboard for exploring anthropometric (body measurement) data across demographic groups. Built with Python and Dash, this tool demonstrates how complex population-level body measurement data can be made accessible and explorable through a reactive web interface — a core challenge in human factors research and ergonomic design tooling.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Dash](https://img.shields.io/badge/Dash-2.x-informational?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-5.x-blueviolet?style=flat-square)

---

## Overview

Human body shape and measurement data underpins the design of vehicles, workspaces, medical devices, and safety systems. This dashboard provides an interactive lens into a synthetic population dataset modeled on NHANES (National Health and Nutrition Examination Survey) anthropometric distributions — allowing researchers and designers to explore how measurements like height, weight, BMI, waist circumference, and sitting height vary across sex and age groups.

All filters update every chart and metric card simultaneously through a single reactive callback, with no page reloads.

---

## Features

- **Live sidebar filters** — filter by sex, age group, and BMI category; all outputs update instantly
- **Summary metrics** — participant count, average height, and average weight update in real time
- **Height vs Weight scatter** — visualize body size relationships by sex with hover details
- **BMI by Age Group box plot** — compare BMI distributions across life stages
- **Height distribution histogram** — overlaid by sex to reveal population shape differences
- **Waist vs Sitting Height scatter** — with OLS trend lines, relevant to seated ergonomic design

---

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Dash](https://dash.plotly.com/) by Plotly |
| Charts | [Plotly Express](https://plotly.com/python/plotly-express/) |
| UI components | [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) |
| Data processing | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| Trend lines | [Statsmodels](https://www.statsmodels.org/) (via Plotly OLS) |

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/dash-body-explorer.git
cd dash-body-explorer

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

Open your browser to `http://127.0.0.1:8050`

---

## Project Structure

```
dash-body-explorer/
├── app.py               # Main application — data, layout, and callbacks
├── requirements.txt     # Pinned dependencies for reproducibility
├── assets/              # Static files (CSS overrides, images)
└── README.md
```

---

## Data

The dataset is synthetically generated at runtime using NumPy, seeded for reproducibility (`seed=42`). Measurement distributions are modeled on published NHANES means and standard deviations for adult males and females:

| Measurement | Male (mean ± SD) | Female (mean ± SD) |
|---|---|---|
| Height (cm) | 175.7 ± 7.1 | 162.1 ± 6.8 |
| Weight (kg) | 88.8 ± 20.1 | 75.4 ± 21.7 |
| Waist (cm) | 96.9 ± 15.2 | 88.7 ± 16.1 |

No external data download is required. The app generates and loads the dataset on startup.

---

## Architecture Note

This app uses Dash's **callback pattern** for all interactivity. A single `@app.callback` function accepts the three filter components as `Input` and drives seven `Output` elements — the three metric cards and four charts. This mirrors the API-backed architecture used in production research tools, where a backend computes model outputs and the frontend renders them reactively.

---

## Author

**Ugonna Okoronkwo**  
B.S. Computer Science, University of Michigan  
[linkedin.com/in/ugonna-okoronkwo](https://linkedin.com/in/ugonna-okoronkwo) · [github.com/ugonnao](https://github.com/ugonnao)
