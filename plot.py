import plotly.graph_objects as go


def create_fitness_plot(fitness_history):
    fig = go.Figure()

    if not fitness_history:
        fig.update_layout(
            title="Динамика fitness",
            xaxis_title="Поколение",
            yaxis_title="Fitness",
        )
        return fig

    generations = [
        point["generation"]
        for point in fitness_history
    ]

    best_values = [
        point["best_fitness"]
        for point in fitness_history
    ]

    avg_values = [
        point["avg_fitness"]
        for point in fitness_history
    ]

    fig.add_trace(
        go.Scatter(
            x=generations,
            y=best_values,
            mode="lines+markers",
            line=dict(color="#ff3b3b", width=3),
            name="Лучший fitness"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=generations,
            y=avg_values,
            mode="lines+markers",
            name="Средний fitness",
            line=dict(color="#ffffff", width=3)
        )
    )

    fig.update_layout(
        xaxis_title="Поколение",
        yaxis_title="Fitness",
        legend_title="Легенда",
    )

    return fig