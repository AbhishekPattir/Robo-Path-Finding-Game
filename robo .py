import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import random
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import time

GRID_SIZE = 20
CELL_SIZE = 30

class RoboPathFindingApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("🤖 Robo Path Finding Game")
        self.geometry(f"{GRID_SIZE * CELL_SIZE + 250}x{GRID_SIZE * CELL_SIZE + 100}")
        self.resizable(False, False)

        # Grid and state
        self.grid_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.goal = None
        self.drawing = False
        
        # Game features
        self.score = 0
        self.level = 1
        self.moves = 0
        self.best_score = 0
        self.start_time = None
        self.is_animating = False
        self.visited_cells = set()

        # Selected algorithm variable
        self.alg_choice = tk.StringVar(value="A*")

        # Load images
        self.load_images()

        # Setup UI
        self.create_widgets()

    def load_images(self):
        """Load robot and flag images"""
        try:
            # Robot image (skeleton character)
            robot_url = "https://agi-prod-file-upload-public-main-use1.s3.amazonaws.com/3b0d6b78-0ad8-47d5-92da-e97ef0fd7b41"
            with urllib.request.urlopen(robot_url) as url:
                robot_data = url.read()
            robot_img = Image.open(BytesIO(robot_data))
            robot_img = robot_img.resize((CELL_SIZE-4, CELL_SIZE-4), Image.Resampling.LANCZOS)
            self.robot_image = ImageTk.PhotoImage(robot_img)

            # Flag image (finish flag)
            flag_url = "https://agi-prod-file-upload-public-main-use1.s3.amazonaws.com/262c8807-ba90-47c0-99b6-d72bc47f52cf"
            with urllib.request.urlopen(flag_url) as url:
                flag_data = url.read()
            flag_img = Image.open(BytesIO(flag_data))
            flag_img = flag_img.resize((CELL_SIZE-4, CELL_SIZE-4), Image.Resampling.LANCZOS)
            self.flag_image = ImageTk.PhotoImage(flag_img)
            
        except Exception as e:
            print(f"Error loading images: {e}")
            self.robot_image = None
            self.flag_image = None

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for grid
        self.canvas = tk.Canvas(main_frame, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, 
                               bg="#2a2a2a", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_right_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release)
        self.draw_grid()

        # Controls Frame
        control_frame = tk.Frame(main_frame, width=250, bg="#1a1a1a")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Title
        title_label = tk.Label(control_frame, text="🤖 ROBO PATH", 
                font=("Arial", 16, "bold"), bg="#1a1a1a", fg="#00d4ff")
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(control_frame, text="FINDING GAME", 
                font=("Arial", 12, "bold"), bg="#1a1a1a", fg="#00d4ff")
        subtitle_label.pack(pady=(0, 10))

        # Stats Frame
        stats_frame = tk.Frame(control_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=10)

        # Level
        self.level_label = tk.Label(stats_frame, text=f"LEVEL: {self.level}", 
                                    font=("Arial", 11, "bold"), bg="#2a2a2a", fg="#FFD700")
        self.level_label.pack(pady=5)

        # Score
        self.score_label = tk.Label(stats_frame, text=f"SCORE: {self.score}", 
                                    font=("Arial", 11, "bold"), bg="#2a2a2a", fg="#00ff00")
        self.score_label.pack(pady=5)

        # Best Score
        self.best_label = tk.Label(stats_frame, text=f"BEST: {self.best_score}", 
                                   font=("Arial", 10), bg="#2a2a2a", fg="#ff9800")
        self.best_label.pack(pady=5)

        # Timer
        self.timer_label = tk.Label(stats_frame, text="TIME: 0:00", 
                                    font=("Arial", 10), bg="#2a2a2a", fg="#ffffff")
        self.timer_label.pack(pady=5)

        # Algorithm selection
        tk.Label(control_frame, text="⚙️ Algorithm:", bg="#1a1a1a", fg="#ffffff",
                font=("Arial", 10, "bold")).pack(pady=(10, 5))
        alg_menu = ttk.Combobox(control_frame, textvariable=self.alg_choice, 
                                values=["A*", "Dijkstra", "BFS", "DFS"], 
                                state="readonly", width=15, font=("Arial", 10))
        alg_menu.pack()

        # Difficulty selector
        tk.Label(control_frame, text="🎯 Difficulty:", bg="#1a1a1a", fg="#ffffff",
                font=("Arial", 10, "bold")).pack(pady=(10, 5))
        self.difficulty = tk.StringVar(value="Medium")
        difficulty_menu = ttk.Combobox(control_frame, textvariable=self.difficulty, 
                                      values=["Easy", "Medium", "Hard", "Expert"], 
                                      state="readonly", width=15, font=("Arial", 10))
        difficulty_menu.pack()

        # Buttons
        button_style = {"font": ("Arial", 10, "bold"), "width": 18, "height": 1, "relief": tk.FLAT, "cursor": "hand2"}

        # Run button with animation
        self.run_button = tk.Button(control_frame, text="🚀 FIND PATH", command=self.find_path, 
                              bg="#00d4ff", fg="#000000", activebackground="#00a8cc", **button_style)
        self.run_button.pack(pady=10)

        # Animate button
        animate_button = tk.Button(control_frame, text="🎬 ANIMATE PATH", command=self.animate_path, 
                                  bg="#9c27b0", fg="white", activebackground="#7b1fa2", **button_style)
        animate_button.pack(pady=5)

        # Generate Maze
        maze_button = tk.Button(control_frame, text="🎲 RANDOM MAZE", 
                               command=self.generate_random_maze, bg="#2196F3", fg="white", 
                               activebackground="#1976D2", **button_style)
        maze_button.pack(pady=5)

        # Next Level
        next_level_button = tk.Button(control_frame, text="⬆️ NEXT LEVEL", 
                                     command=self.next_level, bg="#4CAF50", fg="white",
                                     activebackground="#388E3C", **button_style)
        next_level_button.pack(pady=5)

        # Clear Walls
        clear_walls_button = tk.Button(control_frame, text="🧹 CLEAR WALLS", 
                                       command=self.clear_walls, bg="#FF9800", fg="white",
                                       activebackground="#F57C00", **button_style)
        clear_walls_button.pack(pady=5)

        # Reset
        reset_button = tk.Button(control_frame, text="🔄 RESET GAME", command=self.reset_game, 
                                bg="#f44336", fg="white", activebackground="#d32f2f", **button_style)
        reset_button.pack(pady=5)

        # Instructions
        instructions = tk.Label(control_frame, 
                               text="\n📍 CONTROLS:\n"
                                    "• Left click: Robot & Flag\n"
                                    "• Right drag: Draw walls\n"
                                    "• 🤖 Start | 🏁 Goal\n"
                                    "• Shorter path = Higher score!",
                               bg="#1a1a1a", fg="#aaaaaa", justify=tk.LEFT, font=("Arial", 8))
        instructions.pack(pady=15)

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                
                # Visited cells during pathfinding
                if (i, j) in self.visited_cells:
                    color = "#404040"
                elif self.grid_map[i][j] == 1:
                    color = "#1a1a1a"  # wall
                elif self.start == (i, j):
                    color = "#2d5016"  # dark green for robot
                elif self.goal == (i, j):
                    color = "#4a1a1a"  # dark red for flag
                else:
                    color = "#2a2a2a"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#3a3a3a", width=1)
                
                # Draw images or emojis
                if self.start == (i, j):
                    if self.robot_image:
                        self.canvas.create_image(x1+2, y1+2, anchor=tk.NW, image=self.robot_image)
                    else:
                        self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2, text="🤖", font=("Arial", 16))
                elif self.goal == (i, j):
                    if self.flag_image:
                        self.canvas.create_image(x1+2, y1+2, anchor=tk.NW, image=self.flag_image)
                    else:
                        self.canvas.create_text(x1+CELL_SIZE//2, y1+CELL_SIZE//2, text="🏁", font=("Arial", 16))

    def on_left_click(self, event):
        if self.is_animating:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if row >= GRID_SIZE or col >= GRID_SIZE:
            return
        if self.grid_map[row][col] == 1:
            messagebox.showwarning("⚠️ Warning", "Cannot place on a wall!")
            return
        if not self.start:
            self.start = (row, col)
            self.start_time = time.time()
        elif not self.goal and (row, col) != self.start:
            self.goal = (row, col)
        else:
            messagebox.showinfo("ℹ️ Info", "Robot and flag are set!")
        self.draw_grid()

    def on_right_click(self, event):
        if self.is_animating:
            return
        self.drawing = True
        self.toggle_wall(event)

    def on_right_drag(self, event):
        if self.drawing and not self.is_animating:
            self.toggle_wall(event)

    def on_button_release(self, event):
        self.drawing = False

    def toggle_wall(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if row >= GRID_SIZE or col >= GRID_SIZE or row < 0 or col < 0:
            return
        if (row, col) == self.start or (row, col) == self.goal:
            return
        self.grid_map[row][col] = 1 if self.grid_map[row][col] == 0 else 0
        self.draw_grid()

    def generate_random_maze(self):
        """Generate maze based on difficulty"""
        self.clear_walls()
        difficulty_map = {"Easy": 0.2, "Medium": 0.3, "Hard": 0.4, "Expert": 0.5}
        wall_density = difficulty_map.get(self.difficulty.get(), 0.3)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if random.random() < wall_density:
                    self.grid_map[i][j] = 1
        
        if self.start:
            self.grid_map[self.start[0]][self.start[1]] = 0
        if self.goal:
            self.grid_map[self.goal[0]][self.goal[1]] = 0
        self.draw_grid()

    def clear_walls(self):
        """Clear all walls"""
        self.grid_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.visited_cells.clear()
        self.draw_grid()

    def find_path(self):
        if self.is_animating:
            return
        if not self.start or not self.goal:
            messagebox.showerror("❌ Error", "Place both robot and flag first!")
            return

        self.visited_cells.clear()
        algorithm = self.alg_choice.get()
        
        if algorithm == "A*":
            path = self.astar_search(self.start, self.goal)
        elif algorithm == "Dijkstra":
            path = self.dijkstra_search(self.start, self.goal)
        elif algorithm == "BFS":
            path = self.bfs_search(self.start, self.goal)
        elif algorithm == "DFS":
            path = self.dfs_search(self.start, self.goal)
        else:
            path = None

        if path:
            self.draw_path(path)
            self.calculate_score(path)
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            messagebox.showinfo("🎉 Success!", 
                              f"Path Found!\n\n"
                              f"📊 Algorithm: {algorithm}\n"
                              f"📏 Path Length: {len(path)} steps\n"
                              f"⏱️ Time: {elapsed}s\n"
                              f"🏆 Score: +{self.moves}")
        else:
            messagebox.showwarning("😞 No Path", "Robot can't reach flag!\nTry removing walls.")

    def animate_path(self):
        """Animate the robot moving along the path"""
        if not self.start or not self.goal:
            messagebox.showerror("❌ Error", "Place both robot and flag first!")
            return
        
        if self.is_animating:
            return
        
        algorithm = self.alg_choice.get()
        if algorithm == "A*":
            path = self.astar_search(self.start, self.goal)
        elif algorithm == "Dijkstra":
            path = self.dijkstra_search(self.start, self.goal)
        elif algorithm == "BFS":
            path = self.bfs_search(self.start, self.goal)
        elif algorithm == "DFS":
            path = self.dfs_search(self.start, self.goal)
        else:
            path = None
        
        if not path:
            messagebox.showwarning("😞 No Path", "No path found!")
            return
        
        self.is_animating = True
        self.run_button.config(state=tk.DISABLED)
        self.animate_robot_movement(path, 0)

    def animate_robot_movement(self, path, index):
        """Recursive animation of robot movement"""
        if index >= len(path):
            self.is_animating = False
            self.run_button.config(state=tk.NORMAL)
            self.calculate_score(path)
            messagebox.showinfo("🎉 Arrived!", f"Robot reached the flag!\n🏆 Score: +{self.moves}")
            return
        
        # Update robot position
        old_start = self.start
        self.start = path[index]
        self.visited_cells.add(old_start)
        self.draw_grid()
        
        # Continue animation
        self.after(100, lambda: self.animate_robot_movement(path, index + 1))

    def calculate_score(self, path):
        """Calculate score based on path length and difficulty"""
        base_score = max(100 - len(path), 10)
        difficulty_multiplier = {"Easy": 1, "Medium": 1.5, "Hard": 2, "Expert": 3}
        multiplier = difficulty_multiplier.get(self.difficulty.get(), 1)
        self.moves = int(base_score * multiplier * self.level)
        self.score += self.moves
        
        if self.score > self.best_score:
            self.best_score = self.score
        
        self.update_stats()

    def update_stats(self):
        """Update score display"""
        self.score_label.config(text=f"SCORE: {self.score}")
        self.best_label.config(text=f"BEST: {self.best_score}")
        self.level_label.config(text=f"LEVEL: {self.level}")
        
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"TIME: {minutes}:{seconds:02d}")

    def next_level(self):
        """Progress to next level"""
        self.level += 1
        self.start = None
        self.goal = None
        self.visited_cells.clear()
        self.start_time = time.time()
        self.generate_random_maze()
        messagebox.showinfo("🎮 Level Up!", f"Welcome to Level {self.level}!\nMaze difficulty increased!")

    def draw_path(self, path):
        self.draw_grid()
        for (r, c) in path:
            if (r, c) != self.start and (r, c) != self.goal:
                x1, y1 = c * CELL_SIZE + 8, r * CELL_SIZE + 8
                x2, y2 = x1 + 14, y1 + 14
                self.canvas.create_oval(x1, y1, x2, y2, fill="#00d4ff", outline="#0099cc", width=2)

    def get_neighbors(self, state):
        """Get valid neighbors"""
        r, c = state
        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and self.grid_map[nr][nc] == 0:
                neighbors.append((nr,nc))
        return neighbors

    # Pathfinding algorithms (same as before)
    def astar_search(self, start, goal):
        def heuristic(s):
            return abs(s[0] - goal[0]) + abs(s[1] - goal[1])

        open_set = []
        heapq.heappush(open_set, (0 + heuristic(start), 0, start, None))
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            _, g, current, parent = heapq.heappop(open_set)
            if current == goal:
                path = [current]
                while parent:
                    path.append(parent)
                    parent = came_from.get(parent)
                return path[::-1]
            if current in came_from:
                continue
            came_from[current] = parent
            for neighbor in self.get_neighbors(current):
                new_cost = g + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor)
                    heapq.heappush(open_set, (priority, new_cost, neighbor, current))
        return None

    def dijkstra_search(self, start, goal):
        queue = [(0, start, None)]
        distances = {start: 0}
        came_from = {}

        while queue:
            dist, current, parent = heapq.heappop(queue)
            if current == goal:
                path = [current]
                while parent:
                    path.append(parent)
                    parent = came_from.get(parent)
                return path[::-1]
            if current in came_from:
                continue
            came_from[current] = parent
            for neighbor in self.get_neighbors(current):
                new_dist = dist + 1
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor, current))
        return None

    def bfs_search(self, start, goal):
        from collections import deque
        queue = deque([(start, None)])
        came_from = {start: None}

        while queue:
            current, parent = queue.popleft()
            if current == goal:
                path = [current]
                while came_from[current]:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append((neighbor, current))
        return None

    def dfs_search(self, start, goal):
        stack = [(start, None)]
        came_from = {}
        visited = set()

        while stack:
            current, parent = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            came_from[current] = parent
            if current == goal:
                path = [current]
                while came_from[current]:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, current))
        return None

    def reset_game(self):
        """Complete game reset"""
        self.start = None
        self.goal = None
        self.grid_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.level = 1
        self.moves = 0
        self.start_time = None
        self.visited_cells.clear()
        self.is_animating = False
        self.update_stats()
        self.draw_grid()

if __name__ == "__main__":
    app = RoboPathFindingApp()
    app.mainloop()
