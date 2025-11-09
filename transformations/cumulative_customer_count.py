import pandas as pd
import plotly.express as px

def cumulative_customer_count(customer_df: pd.DataFrame):
    """Create a cumulative customer count bar chart grouped by year-month."""

    # Ensure datetime column
    customer_df['created_at'] = pd.to_datetime(customer_df['created_at'])

    # Extract year-month (YYYY-MM)
    customer_df['yearmonth'] = customer_df['created_at'].dt.to_period('M').astype(str)

    # Count new customers per month
    monthly_counts = (
        customer_df.groupby('yearmonth')
        .agg(new_customers=('id', 'count'))
        .reset_index()
        .sort_values('yearmonth')
    )

    # Cumulative total
    monthly_counts['cumulative_customers'] = monthly_counts['new_customers'].cumsum()

    # Create bar chart
    fig = px.bar(
        monthly_counts,
        x='yearmonth',
        y='cumulative_customers',
        labels={'yearmonth': 'Year-Month', 'cumulative_customers': ''},
        text='cumulative_customers'
    )

    # Modern styling
    fig.update_traces(
        marker_color='#4C78A8',
        marker_line_color='rgba(0,0,0,0)',
        texttemplate='%{text:,}',
        textposition='outside'
    )

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(tickangle=-45, title=None),
        # yaxis=dict(title="Cumulative Customers"),
        margin=dict(t=40, b=60, l=50, r=30),
        hovermode="x unified",
        height=260,
        showlegend=False
    )

    return fig
