#  A* Pathfinding Visualizer (Streamlit)

An interactive A* pathfinding visualizer built with Streamlit and Pillow. This project allows users to set a start and end point, draw barriers, and visualize the A* pathfinding algorithm step-by-step in a grid.

---

##  Features

-  20x20 customizable grid
-  Set Start and End points using side panel controls
-  Draw and clear barriers (obstacles)
-  Step-by-step visualization of the A* algorithm
-  Navigation through steps using "Next", "Previous", and "Restart" buttons
-  Realtime rendering with smooth transitions using PIL

---

##  UI Preview

| Grid View | Controls |
|-----------|----------|
| Grid canvas showing cells and their states | Side panel to select actions and trigger the algorithm |

---

##  Technologies Used

- [Streamlit](https://streamlit.io/) – For web interface and interactivity
- [Pillow (PIL)](https://python-pillow.org/) – For drawing the grid and visual states

---

##  Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/a-star-streamlit.git
cd a-star-streamlit
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

---

##  File Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```

---

##  How to Use

1. Open the sidebar and select an action: **Start**, **End**, **Barrier**, or **Clear**.
2. Choose a cell by providing row and column values (0 to 19).
3. Click **Apply Click** to apply your action.
4. After setting Start and End points, click **Start A* Algorithm** to visualize the path.
5. Use **Previous**, **Restart**, or **Next** buttons to step through the animation.

---

##  Notes

- Barriers cannot overwrite Start or End nodes.
- You must define both a Start and End point before running the algorithm.
- Algorithm uses Manhattan distance as heuristic (H score).

---

##  A* Algorithm Basics

- **Heuristic (H)**: Manhattan Distance
- **Cost (G)**: Cost to move from start node to current
- **F = G + H**: Total estimated cost of the path through the current node

---

##  Author

- **M. Sabtain Khan**
- GitHub: [@Sabtain-Dev](https://github.com/Sabtain-Dev)

---

##  License

This project is licensed under the MIT License.