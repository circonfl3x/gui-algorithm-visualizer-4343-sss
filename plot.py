import plotly.graph_objects as go


def create_fitness_plot(fitness_history):
    fig = go.Figure()

    if fitness_history:
        generations = [
            point["generation"]
            for point in fitness_history
        ]

        population_count = len(
            fitness_history[0]["population_fitness"]
        )

        # Отдельная линия для каждой популяции
        for population_index in range(population_count):
            population_values = [
                point["population_fitness"][population_index]
                for point in fitness_history
            ]

            fig.add_trace(
                go.Scatter(
                    x=generations,
                    y=population_values,
                    mode="lines",
                    line=dict(width=1.5),
                    name=f"Популяция {population_index + 1}",
                )
            )

        best_values = [
            point["best_fitness"]
            for point in fitness_history
        ]

        avg_values = [
            point["avg_fitness"]
            for point in fitness_history
        ]

        # Лучший результат среди всех популяций
        fig.add_trace(
            go.Scatter(
                x=generations,
                y=best_values,
                mode="lines",
                line=dict(
                    width=4,
                    color="#ff3b3b",
                ),
                name="Лучший fitness",
            )
        )

        # Средний результат
        fig.add_trace(
            go.Scatter(
                x=generations,
                y=avg_values,
                mode="lines",
                line=dict(
                    width=3,
                    dash="dash",
                ),
                name="Средний fitness",
            )
        )

    fig.update_layout(
        title="Динамика fitness",
        xaxis_title="Поколение",
        yaxis_title="Fitness",
        legend_title="Легенда",
        hovermode="x unified",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    return fig