import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="JS Pac-Man", page_icon="👻", layout="centered")

st.title("JS Pac-Man")
st.caption("Use Arrow keys or WASD to move. Click inside the game area first so it captures keyboard input.")

PACMAN_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>JS Pac-Man</title>
  <style>
    body {
      background: #111;
      color: #fff;
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 0;
      padding: 10px;
    }
    #game-container {
      text-align: center;
    }
    #score-board {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 10px;
      color: #ffeb3b;
    }
    canvas {
      border: 3px solid #1a237e;
      background-color: #000;
      box-shadow: 0 0 15px rgba(33, 150, 243, 0.4);
    }
  </style>
</head>
<body>
  <div id="game-container">
    <div id="score-board">SCORE: <span id="score">0</span></div>
    <canvas id="canvas" width="380" height="380" tabindex="0"></canvas>
  </div>

  <script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("score");

    // Focus canvas so arrow keys work immediately inside the iframe
    canvas.focus();
    canvas.addEventListener("click", () => canvas.focus());

    const TILE_SIZE = 20;
    const GRID_SIZE = 19;

    // 1: Wall, 0: Pellet, 2: Empty, 3: Power Pellet
    const map = [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
      [1,3,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,3,1],
      [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
      [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
      [1,1,1,1,0,1,1,1,2,1,2,1,1,1,0,1,1,1,1],
      [2,2,2,1,0,1,2,2,2,2,2,2,2,1,0,1,2,2,2],
      [1,1,1,1,0,1,2,1,1,2,1,1,2,1,0,1,1,1,1],
      [2,2,2,2,0,2,2,1,2,2,2,1,2,2,0,2,2,2,2],
      [1,1,1,1,0,1,2,1,1,1,1,1,2,1,0,1,1,1,1],
      [2,2,2,1,0,1,2,2,2,2,2,2,2,1,0,1,2,2,2],
      [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
      [1,3,0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,3,1],
      [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];

    let score = 0;
    let gameOver = false;
    let victory = false;

    const pacman = {
      x: 9,
      y: 16,
      dirX: 0,
      dirY: 0,
      nextDirX: 0,
      nextDirY: 0,
      mouthOpen: 0.2,
      mouthSpeed: 0.04
    };

    const ghost = {
      x: 9,
      y: 8,
      dirX: 0,
      dirY: -1,
      color: "#ff3333"
    };

    function canMoveTo(x, y) {
      if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) return false;
      return map[y][x] !== 1;
    }

    canvas.addEventListener("keydown", (e) => {
      switch (e.key) {
        case "ArrowUp":
        case "w":
          pacman.nextDirX = 0;
          pacman.nextDirY = -1;
          e.preventDefault();
          break;
        case "ArrowDown":
        case "s":
          pacman.nextDirX = 0;
          pacman.nextDirY = 1;
          e.preventDefault();
          break;
        case "ArrowLeft":
        case "a":
          pacman.nextDirX = -1;
          pacman.nextDirY = 0;
          e.preventDefault();
          break;
        case "ArrowRight":
        case "d":
          pacman.nextDirX = 1;
          pacman.nextDirY = 0;
          e.preventDefault();
          break;
      }
    });

    function updateGhost() {
      const possibleMoves = [
        { dx: 0, dy: -1 },
        { dx: 0, dy: 1 },
        { dx: -1, dy: 0 },
        { dx: 1, dy: 0 }
      ].filter(m => {
        const isReverse = m.dx === -ghost.dirX && m.dy === -ghost.dirY;
        return canMoveTo(ghost.x + m.dx, ghost.y + m.dy) && !isReverse;
      });

      let move;
      if (possibleMoves.length > 0) {
        possibleMoves.sort((a, b) => {
          const distA = Math.hypot((ghost.x + a.dx) - pacman.x, (ghost.y + a.dy) - pacman.y);
          const distB = Math.hypot((ghost.x + b.dx) - pacman.x, (ghost.y + b.dy) - pacman.y);
          return distA - distB;
        });
        move = Math.random() < 0.7 ? possibleMoves[0] : possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
      } else {
        move = { dx: -ghost.dirX, dy: -ghost.dirY };
      }

      if (move && canMoveTo(ghost.x + move.dx, ghost.y + move.dy)) {
        ghost.dirX = move.dx;
        ghost.dirY = move.dy;
        ghost.x += ghost.dirX;
        ghost.y += ghost.dirY;
      }
    }

    function updatePacman() {
      if (canMoveTo(pacman.x + pacman.nextDirX, pacman.y + pacman.nextDirY)) {
        pacman.dirX = pacman.nextDirX;
        pacman.dirY = pacman.nextDirY;
      }

      if (canMoveTo(pacman.x + pacman.dirX, pacman.y + pacman.dirY)) {
        pacman.x += pacman.dirX;
        pacman.y += pacman.dirY;
      }

      const currentTile = map[pacman.y][pacman.x];
      if (currentTile === 0) {
        map[pacman.y][pacman.x] = 2;
        score += 10;
        scoreEl.innerText = score;
      } else if (currentTile === 3) {
        map[pacman.y][pacman.x] = 2;
        score += 50;
        scoreEl.innerText = score;
      }

      const remaining = map.flat().filter(tile => tile === 0 || tile === 3).length;
      if (remaining === 0) victory = true;

      if (pacman.x === ghost.x && pacman.y === ghost.y) {
        gameOver = true;
      }
    }

    function draw() {
      ctx.fillStyle = "#000";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let r = 0; r < GRID_SIZE; r++) {
        for (let c = 0; c < GRID_SIZE; c++) {
          const type = map[r][c];
          const px = c * TILE_SIZE;
          const py = r * TILE_SIZE;

          if (type === 1) {
            ctx.fillStyle = "#1565c0";
            ctx.fillRect(px, py, TILE_SIZE, TILE_SIZE);
          } else if (type === 0) {
            ctx.fillStyle = "#ffb74d";
            ctx.beginPath();
            ctx.arc(px + 10, py + 10, 2.5, 0, Math.PI * 2);
            ctx.fill();
          } else if (type === 3) {
            ctx.fillStyle = "#fff";
            ctx.beginPath();
            ctx.arc(px + 10, py + 10, 5, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      const gx = ghost.x * TILE_SIZE + 10;
      const gy = ghost.y * TILE_SIZE + 10;
      ctx.fillStyle = ghost.color;
      ctx.beginPath();
      ctx.arc(gx, gy - 2, 8, Math.PI, 0, false);
      ctx.lineTo(gx + 8, gy + 8);
      ctx.lineTo(gx - 8, gy + 8);
      ctx.fill();

      ctx.fillStyle = "#fff";
      ctx.beginPath();
      ctx.arc(gx - 3, gy - 2, 2.5, 0, Math.PI * 2);
      ctx.arc(gx + 3, gy - 2, 2.5, 0, Math.PI * 2);
      ctx.fill();

      const px = pacman.x * TILE_SIZE + 10;
      const py = pacman.y * TILE_SIZE + 10;
      let angle = 0;
      if (pacman.dirX === 1) angle = 0;
      if (pacman.dirX === -1) angle = Math.PI;
      if (pacman.dirY === 1) angle = 0.5 * Math.PI;
      if (pacman.dirY === -1) angle = 1.5 * Math.PI;

      pacman.mouthOpen += pacman.mouthSpeed;
      if (pacman.mouthOpen > 0.25 || pacman.mouthOpen < 0.02) {
        pacman.mouthSpeed = -pacman.mouthSpeed;
      }

      ctx.fillStyle = "#ffeb3b";
      ctx.beginPath();
      ctx.arc(
        px, py, 8,
        angle + pacman.mouthOpen * Math.PI,
        angle + (2 - pacman.mouthOpen) * Math.PI
      );
      ctx.lineTo(px, py);
      ctx.fill();

      if (gameOver || victory) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = victory ? "#4caf50" : "#f44336";
        ctx.font = "bold 24px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(victory ? "YOU WIN!" : "GAME OVER", canvas.width / 2, canvas.height / 2);
      }
    }

    let lastTick = 0;
    function gameLoop(timestamp) {
      if (!gameOver && !victory) {
        if (timestamp - lastTick > 160) {
          updatePacman();
          updateGhost();
          lastTick = timestamp;
        }
      }
      draw();
      if (!gameOver && !victory) {
        requestAnimationFrame(gameLoop);
      }
    }

    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

components.html(PACMAN_HTML, height=460, scrolling=False)
