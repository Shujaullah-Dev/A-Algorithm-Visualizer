import streamlit as st
from PIL import Image, ImageDraw
import time
import heapq

# Constants
ROWS = 20
COLS = 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
GREY = (200, 200, 200)

def init_state():
    if "grid" not in st.session_state:
        st.session_state.grid = [["empty" for _ in range(COLS)] for _ in range(ROWS)]
        st.session_state.start = None
        st.session_state.end = None
        st.session_state.path = []
        st.session_state.animating = False
        st.session_state.history = []
        st.session_state.history_index = -1

def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star(draw_callback):
    start = st.session_state.start
    end = st.session_state.end
    if not start or not end:
        return False

    came_from = {}
    g_score = {(r, c): float("inf") for r in range(ROWS) for c in range(COLS)}
    f_score = {(r, c): float("inf") for r in range(ROWS) for c in range(COLS)}
    g_score[start] = 0
    f_score[start] = h(start, end)

    open_set = [(f_score[start], 0, start)]
    open_set_hash = {start}
    count = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                if current != start:
                    st.session_state.grid[current[0]][current[1]] = "path"
                save_frame()
                draw_callback()
                time.sleep(0.02)
            return True

        neighbors = get_neighbors(current)
        for neighbor in neighbors:
            if st.session_state.grid[neighbor[0]][neighbor[1]] == "barrier":
                continue

            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        st.session_state.grid[neighbor[0]][neighbor[1]] = "open"
        if current != start:
            st.session_state.grid[current[0]][current[1]] = "closed"
        save_frame()
        draw_callback()
        time.sleep(0.02)

    return False

def save_frame():
    snapshot = [row.copy() for row in st.session_state.grid]
    st.session_state.history.append(snapshot)
    st.session_state.history_index = len(st.session_state.history) - 1

def next_step():
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history_index += 1
        st.session_state.grid = [row.copy() for row in st.session_state.history[st.session_state.history_index]]

def prev_step():
    if st.session_state.history_index > 0:
        st.session_state.history_index -= 1
        st.session_state.grid = [row.copy() for row in st.session_state.history[st.session_state.history_index]]

def restart_step():
    if st.session_state.history:
        st.session_state.history_index = 0
        st.session_state.grid = [row.copy() for row in st.session_state.history[0]]

def get_neighbors(pos):
    r, c = pos
    neighbors = []
    if r > 0: neighbors.append((r-1, c))
    if r < ROWS - 1: neighbors.append((r+1, c))
    if c > 0: neighbors.append((r, c-1))
    if c < COLS - 1: neighbors.append((r, c+1))
    return neighbors

def draw_grid():
    img = Image.new("RGB", (WIDTH + 50, HEIGHT + 50), color=WHITE)
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            x0 = c * CELL_SIZE + 50
            y0 = r * CELL_SIZE + 50
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            color = WHITE
            state = st.session_state.grid[r][c]
            if state == "barrier": color = BLACK
            elif state == "start": color = ORANGE
            elif state == "end": color = TURQUOISE
            elif state == "open": color = GREEN
            elif state == "closed": color = RED
            elif state == "path": color = PURPLE
            draw.rectangle([x0, y0, x1, y1], fill=color)
            draw.rectangle([x0, y0, x1, y1], outline=GREY)

    for r in range(ROWS):
        draw.text((30, r * CELL_SIZE + 55), str(r), fill=BLACK)
    for c in range(COLS):
        draw.text((c * CELL_SIZE + 55, 30), str(c), fill=BLACK)

    return img

# UI
st.set_page_config(layout="wide")
init_state()
st.markdown("<style>body { overflow: hidden; }</style>", unsafe_allow_html=True)

cols = st.columns([1, 4])

with cols[0]:
    st.sidebar.title("Controls")
    selected_action = st.sidebar.radio("Action", ["Start", "End", "Barrier", "Clear"], index=2)
    clicked_row = st.sidebar.number_input("Row (0-indexed)", 0, ROWS - 1, 0)
    clicked_col = st.sidebar.number_input("Col (0-indexed)", 0, COLS - 1, 0)

    if st.sidebar.button("Apply Click"):
        r, c = clicked_row, clicked_col
        if selected_action == "Start":
            if st.session_state.start:
                r0, c0 = st.session_state.start
                st.session_state.grid[r0][c0] = "empty"
            st.session_state.grid[r][c] = "start"
            st.session_state.start = (r, c)
        elif selected_action == "End":
            if st.session_state.end:
                r0, c0 = st.session_state.end
                st.session_state.grid[r0][c0] = "empty"
            st.session_state.grid[r][c] = "end"
            st.session_state.end = (r, c)
        elif selected_action == "Barrier":
            if (r, c) != st.session_state.start and (r, c) != st.session_state.end:
                st.session_state.grid[r][c] = "barrier"
        elif selected_action == "Clear":
            if (r, c) == st.session_state.start:
                st.session_state.start = None
            if (r, c) == st.session_state.end:
                st.session_state.end = None
            st.session_state.grid[r][c] = "empty"

    if st.sidebar.button("Start A* Algorithm"):
        st.session_state.history = []
        save_frame()
        a_star(lambda: None)
        st.session_state.grid = [row.copy() for row in st.session_state.history[-1]]
        st.session_state.history_index = len(st.session_state.history) - 1

    if st.sidebar.button("Reset Grid"):
        st.session_state.grid = [["empty" for _ in range(COLS)] for _ in range(ROWS)]
        st.session_state.start = None
        st.session_state.end = None
        st.session_state.history = []
        st.session_state.history_index = -1

with cols[1]:
    st.image(draw_grid(), use_container_width=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("⬅ Previous Step", on_click=prev_step, disabled=st.session_state.history_index <= 0)
    with col2:
        st.button("⏮ Restart to First Step", on_click=restart_step, disabled=st.session_state.history_index <= 0)
    with col3:
        st.button("Next Step ➡", on_click=next_step, disabled=st.session_state.history_index >= len(st.session_state.history) - 1)
