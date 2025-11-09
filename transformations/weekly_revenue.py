import pandas as pd
import plotly.express as px

def weekly_revenue(df: pd.DataFrame):

    # Make a copy to avoid modifying original DataFrame
    df = df.copy()

    # Ensure created_at is datetime
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    # Derive year-week column (ISO week)
    df["yearweek"] = df["created_at"].dt.strftime("%Y-%U")

    # Group by yearweek and sum total
    weekly = (
        df.groupby("yearweek", as_index=False)["total"]
        .sum()
        .sort_values("yearweek")
    )

    # Create line chart
    fig = px.line(
        weekly,
        x="yearweek",
        y="total",
        markers=True
        )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        hovermode="x unified",
        template="plotly_white",
        height=260
    )

    return fig
