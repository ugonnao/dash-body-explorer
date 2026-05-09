import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

# =============================================================
# 1. DATA — synthetic NHANES-inspired anthropometric dataset
# =============================================================
np.random.seed(42)
n = 600

sexes = np.random.choice(["Male", "Female"], size=n)
ages  = np.random.randint(18, 80, size=n)

heights = np.where(
    sexes == "Male",
    np.random.normal(175.7, 7.1, n),
    np.random.normal(162.1, 6.8, n),
)
weights = np.where(
    sexes == "Male",
    np.random.normal(88.8, 20.1, n),
    np.random.normal(75.4, 21.7, n),
)
bmi            = weights / ((heights / 100) ** 2)
waist          = np.where(sexes == "Male",
                           np.random.normal(96.9, 15.2, n),
                           np.random.normal(88.7, 16.1, n))
sitting_height = heights * np.random.uniform(0.51, 0.53, n)

age_groups = pd.cut(
    ages,
    bins=[17, 29, 44, 59, 79],
    labels=["18–29", "30–44", "45–59", "60–79"],
)
bmi_categories = pd.cut(
    bmi,
    bins=[0, 18.5, 25, 30, 100],
    labels=["Underweight", "Normal", "Overweight", "Obese"],
)

df = pd.DataFrame({
    "Sex":               sexes,
    "Age":               ages,
    "Age Group":         age_groups,
    "Height (cm)":       heights.round(1),
    "Weight (kg)":       weights.round(1),
    "BMI":               bmi.round(1),
    "BMI Category":      bmi_categories,
    "Waist (cm)":        waist.round(1),
    "Sitting Height (cm)": sitting_height.round(1),
})

COLOR_MAP = {"Male": "#185FA5", "Female": "#993556"}

# =============================================================
# 2. APP INIT
# =============================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Human Body Measurement Explorer"

# =============================================================
# 3. LAYOUT
# =============================================================

# -- Sidebar filters --
sidebar = dbc.Card([
    html.H5("Filters", className="mb-3 fw-semibold"),

    html.Label("Sex", className="fw-semibold text-muted", style={"fontSize": "12px"}),
    dcc.Checklist(
        id="sex-filter",
        options=[{"label": "  Male", "value": "Male"},
                 {"label": "  Female", "value": "Female"}],
        value=["Male", "Female"],
        className="mb-3",
    ),

    html.Label("Age Group", className="fw-semibold text-muted", style={"fontSize": "12px"}),
    dcc.Checklist(
        id="age-filter",
        options=[{"label": f"  {g}", "value": g}
                 for g in ["18–29", "30–44", "45–59", "60–79"]],
        value=["18–29", "30–44", "45–59", "60–79"],
        className="mb-3",
    ),

    html.Label("BMI Category", className="fw-semibold text-muted", style={"fontSize": "12px"}),
    dcc.Checklist(
        id="bmi-filter",
        options=[{"label": f"  {c}", "value": c}
                 for c in ["Underweight", "Normal", "Overweight", "Obese"]],
        value=["Underweight", "Normal", "Overweight", "Obese"],
        className="mb-3",
    ),

    html.Hr(),
    html.P(
        "Data: synthetic population modeled on NHANES anthropometric distributions.",
        className="text-muted",
        style={"fontSize": "11px"},
    ),
], body=True, className="shadow-sm")

# -- Summary metric cards --
def metric_card(label, id_):
    return dbc.Col(
        dbc.Card([
            html.P(label, className="text-muted mb-1", style={"fontSize": "12px"}),
            html.H4(id=id_, className="mb-0 fw-semibold"),
        ], body=True, className="shadow-sm text-center"),
        width=4,
    )

metric_row = dbc.Row([
    metric_card("Participants",     "metric-count"),
    metric_card("Avg Height (cm)", "metric-height"),
    metric_card("Avg Weight (kg)", "metric-weight"),
], className="mb-4")

# -- Full page layout --
app.layout = dbc.Container([

    dbc.Row(dbc.Col(html.Div([
        html.H3("Human Body Measurement Explorer", className="mb-0 mt-3"),
        html.P(
            "Interactive exploration of synthetic anthropometric data — modeled on NHANES population distributions",
            className="text-muted",
            style={"fontSize": "13px"},
        ),
    ]))),

    html.Hr(),

    dbc.Row([
        # Sidebar
        dbc.Col(sidebar, width=3),

        # Main panel
        dbc.Col([
            metric_row,
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="scatter-plot"),  body=True, className="shadow-sm mb-3"), width=7),
                dbc.Col(dbc.Card(dcc.Graph(id="bmi-box"),       body=True, className="shadow-sm mb-3"), width=5),
            ]),
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="height-hist"),   body=True, className="shadow-sm"), width=6),
                dbc.Col(dbc.Card(dcc.Graph(id="waist-scatter"), body=True, className="shadow-sm"), width=6),
            ]),
        ], width=9),
    ]),

], fluid=True)

# =============================================================
# 4. CALLBACKS — the reactive core of Dash
# =============================================================
@app.callback(
    Output("metric-count",    "children"),
    Output("metric-height",   "children"),
    Output("metric-weight",   "children"),
    Output("scatter-plot",    "figure"),
    Output("bmi-box",         "figure"),
    Output("height-hist",     "figure"),
    Output("waist-scatter",   "figure"),
    Input("sex-filter",  "value"),
    Input("age-filter",  "value"),
    Input("bmi-filter",  "value"),
)
def update_dashboard(sex_vals, age_vals, bmi_vals):
    """Single callback drives all outputs from the three filter inputs."""

    filtered = df[
        df["Sex"].isin(sex_vals) &
        df["Age Group"].isin(age_vals) &
        df["BMI Category"].isin(bmi_vals)
    ]

    # Metric cards
    count      = len(filtered)
    avg_height = f"{filtered['Height (cm)'].mean():.1f}" if count else "—"
    avg_weight = f"{filtered['Weight (kg)'].mean():.1f}" if count else "—"

    layout_base = dict(margin=dict(t=45, b=20, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")

    # Chart 1 — Height vs Weight scatter
    scatter = px.scatter(
        filtered, x="Height (cm)", y="Weight (kg)", color="Sex",
        title="Height vs Weight",
        opacity=0.55,
        color_discrete_map=COLOR_MAP,
        hover_data=["Age", "BMI"],
    )
    scatter.update_layout(**layout_base, legend=dict(orientation="h", y=-0.18))

    # Chart 2 — BMI distribution by age group
    box = px.box(
        filtered, x="Age Group", y="BMI", color="Sex",
        title="BMI by Age Group",
        color_discrete_map=COLOR_MAP,
    )
    box.update_layout(**layout_base, showlegend=False)

    # Chart 3 — Height histogram
    hist = px.histogram(
        filtered, x="Height (cm)", color="Sex",
        barmode="overlay", opacity=0.7,
        title="Height Distribution",
        color_discrete_map=COLOR_MAP,
    )
    hist.update_layout(**layout_base, legend=dict(orientation="h", y=-0.18))

    # Chart 4 — Waist vs Sitting Height with trend line
    waist_fig = px.scatter(
        filtered, x="Waist (cm)", y="Sitting Height (cm)", color="Sex",
        title="Waist vs Sitting Height",
        opacity=0.55,
        color_discrete_map=COLOR_MAP,
        trendline="ols",
    )
    waist_fig.update_layout(**layout_base, showlegend=False)

    return count, avg_height, avg_weight, scatter, box, hist, waist_fig


# =============================================================
# 5. RUN
# =============================================================
if __name__ == "__main__":
    app.run(debug=True)
