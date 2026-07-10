import copy

import streamlit as st
import time
from plot import create_fitness_plot
from sudoku_solver import sudoku_io
from classes.GeneticAlgorithm import GeneticAlgorithm as ga


st.set_page_config(page_title="Sudoku GA", layout="wide")

def create_ga(field):
    return ga(
        field,
        population_count=population_count,
        population_size=population_size,
        max_generations=max_generations,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
    )

def set_solver_state(field):
    st.session_state.field = copy.deepcopy(field)
    st.session_state.ga = create_ga(copy.deepcopy(field))

    first_snapshot = st.session_state.ga.get_snapshot()

    st.session_state.snapshots = [first_snapshot]
    st.session_state.snapshot_index = 0

    st.session_state.fitness_history = []
    add_fitness_point(first_snapshot, force=True)

    st.session_state.running = False
    st.session_state.fast_mode = False
    
def new_puzzle():
    _, field_np = sudoku_io.generate_puzzle()

    img = sudoku_io.field_to_img(field_np)
    img.save("sudoku_solver/puzzle.png")

    set_solver_state(field_np)

def reset_solver():
    if "field" not in st.session_state:
        new_puzzle()
        return

    set_solver_state(st.session_state.field)

def get_current_snapshot():
    return st.session_state.snapshots[st.session_state.snapshot_index]

def step_forward():
    if "ga" not in st.session_state:
        new_puzzle()

    if st.session_state.snapshot_index < len(st.session_state.snapshots) - 1:
        st.session_state.snapshot_index += 1
        return

    snapshot = st.session_state.ga.step()

    st.session_state.snapshots.append(snapshot)
    st.session_state.snapshot_index = len(st.session_state.snapshots) - 1

    add_fitness_point(snapshot)

    if snapshot["solved"] or snapshot["generation"] >= st.session_state.ga.max_generations:
        st.session_state.running = False
        st.session_state.fast_mode = False
        
def step_back():
    if "snapshots" not in st.session_state:
        return

    if st.session_state.snapshot_index > 0:
        st.session_state.snapshot_index -= 1

def add_fitness_point(snapshot, force=False):
    generation = snapshot["generation"]

    if not force and generation % 50 != 0:
        return

    if "fitness_history" not in st.session_state:
        st.session_state.fitness_history = []

    if st.session_state.fitness_history:
        last_generation = st.session_state.fitness_history[-1]["generation"]

        if last_generation == generation:
            return

    st.session_state.fitness_history.append(
        {
            "generation": generation,
            "best_fitness": snapshot["best_fitness"],
            "avg_fitness": snapshot["avg_fitness"],
        }
    )

main_col1, main_col2 = st.columns([1,4])
with main_col1:
    with st.container(border=True, horizontal_alignment="center"):
        st.subheader("Параметры алгоритма", text_alignment="center")
        population_count = st.slider(
            "Количество популяций",
            min_value=1,
            max_value=20
        )
        population_size = st.slider(
            "Размер популяции",
            min_value=50, max_value=1000, value=100)
        mutation_rate = st.slider(
            "Вероятность мутации",
            min_value=0.0, max_value=0.30, value=0.05)
        crossover_rate = st.slider(
            "Вероятность скрещивания",
            min_value=0.0, max_value=1.0, value=0.8)
        max_generations = st.slider(
            "Максимальное количество поколений",
            min_value=100, max_value=10000, value=3000)
    if "ga" not in st.session_state:
        new_puzzle()
    with st.container(border=True):
        st.subheader("Управление", text_alignment="center")

        if st.button("Новый паззл", width="stretch", type="primary"):
            new_puzzle()
            st.rerun()

        button_col1, button_col2, button_col3, button_col4 = st.columns(4)

        with button_col1:
            if st.button("Шаг назад", width="stretch"):
                st.session_state.running = False
                st.session_state.fast_mode = False
                step_back()
                st.rerun()

        with button_col2:
            if st.button("Старт", width="stretch"):
                st.session_state.running = True
                st.session_state.fast_mode = False
                st.rerun()

        with button_col3:
            if st.button("Пауза", width="stretch"):
                st.session_state.running = False
                st.session_state.fast_mode = False
                st.rerun()

        with button_col4:
            if st.button("Шаг вперед", width="stretch"):
                st.session_state.running = False
                st.session_state.fast_mode = False
                step_forward()
                st.rerun()

        if st.button("Сброс", width="stretch", type="primary"):
            reset_solver()
            st.rerun()

        if st.button("Конечное решение", width="stretch", type="primary"):
            st.session_state.running = True
            st.session_state.fast_mode = True
            st.rerun()

current_snapshot = get_current_snapshot()

current_matrix = current_snapshot["matrix"]
current_generation = current_snapshot["generation"]
best_fitness = current_snapshot["best_fitness"]
solved = current_snapshot["solved"]
avg_fitness = current_snapshot["avg_fitness"]

with main_col2:
    sudoku_col1, sudoku_col2 = st.columns(2)

    with sudoku_col1:
        with st.container(border=True):
            st.subheader("Исходное поле судоку", text_alignment="center")
            st.image(
                sudoku_io.field_to_img(
                    st.session_state.field,
                    fixed_cells=st.session_state.ga.fixed_cells
                )
            )

    with sudoku_col2:
        with st.container(border=True):
            st.subheader("Лучшее текущее решение", text_alignment="center")
            st.image(
                sudoku_io.field_to_img(
                    current_matrix,
                    fixed_cells=st.session_state.ga.fixed_cells
                )
            )
    with st.container():
        info_col1, info_col2, info_col3= st.columns(3)

        with info_col1:
            with st.container(border=True):
                st.metric("Поколение", current_generation)
        with info_col2:
            with st.container(border=True):
                st.metric("Лучший fitness", best_fitness)
        with info_col3:
            with st.container(border=True):
                st.metric("Средний fitness", round(avg_fitness, 2))

    with st.container(border=True):
        st.subheader("График приспособленности")
        fig = create_fitness_plot(st.session_state.fitness_history)
        st.plotly_chart(fig)


if st.session_state.get("running", False):
    steps_per_rerun = 50 if st.session_state.get("fast_mode", False) else 1

    for _ in range(steps_per_rerun):
        step_forward()

        current_snapshot = get_current_snapshot()

        if current_snapshot["solved"]:
            st.session_state.running = False
            st.session_state.fast_mode = False
            break

        if current_snapshot["generation"] >= st.session_state.ga.max_generations:
            st.session_state.running = False
            st.session_state.fast_mode = False
            break

    time.sleep(0.05)
    st.rerun()