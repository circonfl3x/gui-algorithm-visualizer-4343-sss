import plotly.graph_objects as go
generations = [0, 1, 2, 3, 4, 5]
best_fitness = [120, 96, 74, 55, 41, 28]
avg_fitness = [150, 132, 110, 92, 76, 61]


def create_fitness_plot():
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=generations,
        y=best_fitness,
        mode="lines+markers",
        name="Лучший fitness"
    ))

    fig.add_trace(go.Scatter(
        x=generations,
        y=avg_fitness,
        mode="lines+markers",
        name="Средний fitness"
    ))

    fig.update_layout(
        title="Динамика fitness",
        xaxis_title="Поколение",
        yaxis_title="Fitness",
        template="plotly_dark",
        height=420,
        paper_bgcolor="#171B24",
        plot_bgcolor="#171B24",
        font=dict(color="#F3F4F6"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    fig.update_xaxes(
        gridcolor="#2E3543",
        zerolinecolor="#2E3543"
    )

    fig.update_yaxes(
        gridcolor="#2E3543",
        zerolinecolor="#2E3543"
    )

    return fig