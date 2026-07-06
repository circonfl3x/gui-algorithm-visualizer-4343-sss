import streamlit as st
from plot_template import create_fitness_plot
st.set_page_config(page_title="Sudoku GA", layout="wide")

st.title("Решение судоку")

main_col1, main_col2, main_col3 = st.columns(3)
with main_col1:
    with st.container(border=True, horizontal_alignment="center"):
        st.subheader("Параметры генетического алгоритма")
        population_size = st.slider(
            "Размер популяции",
            min_value=50, max_value=1000, value=100)
        mutation_probability = st.slider(
            "Вероятность мутации",
            min_value=0.0, max_value=0.30, value=0.05)
        crossover_probability = st.slider(
            "Вероятность скрещивания",
            min_value=0.0, max_value=1.0, value=0.8)
        max_generations = st.slider(
            "Максимальное количество поколений",
            min_value=100, max_value=10000, value=3000)
    with st.container(border=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.subheader("Управление")
        with st.container():
            button_col1, button_col2, button_col3, button_col4 = st.columns(4)
            with button_col1:
                st.button("Шаг назад", width="stretch")
            with button_col2:
                st.button("Старт", width="stretch")
            with button_col3:
                st.button("Пауза", width="stretch")
            with button_col4:
                st.button("Шаг вперед", width="stretch")
            st.button("Сброс", width="stretch", type="primary")
with main_col2:
    with st.container(border=True):
        st.subheader("Исходное поле судоку")
with main_col3:
    with st.container(border=True):
        st.subheader("Лучшее текущее решение")
with st.container(border=True):
    st.subheader("График приспособленности")

    fig = create_fitness_plot() # TODO plot

    st.plotly_chart(fig, use_container_width=True)