# Robo Path Finding Game

An interactive Python GUI game built with Tkinter that demonstrates classic pathfinding algorithms like A*, Dijkstra, BFS, and DFS in a fun, visual way.

The player places a robot (start) and a flag (goal), draws walls to create obstacles, and selects an algorithm to find the shortest path.

---

## Features

-  Multiple Pathfinding Algorithms:
  - A* (A-Star)
  - Dijkstra’s Algorithm
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)

-  Game Mechanics:
  - Scoring system
  - Level progression
  - Difficulty modes (Easy, Medium, Hard, Expert)
  - Timer tracking
  - Best score tracking

-  Visual Animation:
  - Animated robot movement
  - Visual path drawing
  - Visited cell highlighting

-  Random Maze Generator
-  Clear walls option
-  Full game reset

---

##  Technologies Used

- Python 3
- Tkinter (GUI)
- Heapq (Priority Queue)
- PIL (Pillow for images)
- Object-Oriented Programming

---

##  Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/robo-path-finding-game.git
cd robo-path-finding-game
```
2.Install required dependencies:
```bash
pip install pillow
```
3.Run the application:
```bash
python main.py
```
 How to Play

 Left Click → Place Robot (Start) and Flag (Goal)

 Right Click & Drag → Draw or Remove Walls

 Select Algorithm → Choose pathfinding method

 Click "Find Path" → Instantly calculate path

 Click "Animate Path" → Watch robot move step-by-step

 Generate random maze for challenge

 Level up for increased difficulty

Shorter path = Higher score!

 Algorithms Overview
A*

Uses a heuristic (Manhattan distance) to efficiently find the shortest path.

Dijkstra

Guarantees shortest path using weighted cost expansion.

BFS

Explores level-by-level. Finds shortest path in unweighted grids.

DFS

Explores deeply before backtracking. May not find shortest path.

 Scoring System

Score is calculated based on:

Path length

Difficulty multiplier

Current level

Higher difficulty + shorter path = More points

 Project Structure
 ```bash
robo-path-finding-game/
│
├── main.py
├── README.md
 ```
Educational Purpose

This project is ideal for:

Understanding pathfinding algorithms visually

Learning Tkinter GUI development

Demonstrating algorithm behavior differences

Academic presentations and seminars

 Future Improvements

Diagonal movement support

Weighted grids

Save/Load maze feature

Algorithm speed comparison chart

Leaderboard system

 Author

Abhishek Pattir

If you found this project helpful, consider giving it a  on GitHub!
