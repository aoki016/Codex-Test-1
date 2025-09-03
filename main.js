const SIZE = 8;
const board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
// 初期配置
board[3][3] = 2;
board[4][4] = 2;
board[3][4] = 1;
board[4][3] = 1;

const boardDiv = document.getElementById('board');
const statusP = document.getElementById('status');
const dirs = [
  [-1, -1], [-1, 0], [-1, 1],
  [0, -1],          [0, 1],
  [1, -1],  [1, 0], [1, 1]
];

function drawBoard() {
  boardDiv.innerHTML = '';
  for (let r = 0; r < SIZE; r++) {
    for (let c = 0; c < SIZE; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.row = r;
      cell.dataset.col = c;
      const val = board[r][c];
      if (val) {
        const disc = document.createElement('div');
        disc.className = 'disc ' + (val === 1 ? 'black' : 'white');
        cell.appendChild(disc);
      }
      boardDiv.appendChild(cell);
    }
  }
}

function inBounds(r, c) {
  return r >= 0 && r < SIZE && c >= 0 && c < SIZE;
}

function isValidMove(r, c, color) {
  if (!inBounds(r, c) || board[r][c] !== 0) return false;
  const opp = color === 1 ? 2 : 1;
  for (const [dr, dc] of dirs) {
    let i = r + dr, j = c + dc;
    let hasOpp = false;
    while (inBounds(i, j) && board[i][j] === opp) {
      i += dr; j += dc; hasOpp = true;
    }
    if (hasOpp && inBounds(i, j) && board[i][j] === color) {
      return true;
    }
  }
  return false;
}

function getValidMoves(color) {
  const moves = [];
  for (let r = 0; r < SIZE; r++) {
    for (let c = 0; c < SIZE; c++) {
      if (isValidMove(r, c, color)) moves.push([r, c]);
    }
  }
  return moves;
}

function applyMove(r, c, color) {
  board[r][c] = color;
  const opp = color === 1 ? 2 : 1;
  for (const [dr, dc] of dirs) {
    let i = r + dr, j = c + dc;
    const toFlip = [];
    while (inBounds(i, j) && board[i][j] === opp) {
      toFlip.push([i, j]);
      i += dr; j += dc;
    }
    if (toFlip.length && inBounds(i, j) && board[i][j] === color) {
      for (const [fr, fc] of toFlip) {
        board[fr][fc] = color;
      }
    }
  }
}

function countFlips(r, c, color) {
  const opp = color === 1 ? 2 : 1;
  let total = 0;
  for (const [dr, dc] of dirs) {
    let i = r + dr, j = c + dc;
    let cnt = 0;
    while (inBounds(i, j) && board[i][j] === opp) {
      cnt++; i += dr; j += dc;
    }
    if (cnt && inBounds(i, j) && board[i][j] === color) {
      total += cnt;
    }
  }
  return total;
}

function aiMove() {
  const moves = getValidMoves(2);
  if (!moves.length) return false;
  let best = null, bestScore = -1;
  for (const [r, c] of moves) {
    const score = countFlips(r, c, 2);
    if (score > bestScore) {
      bestScore = score;
      best = [r, c];
    }
  }
  if (best) applyMove(best[0], best[1], 2);
  return true;
}

function checkGameEnd() {
  const blackMoves = getValidMoves(1);
  const whiteMoves = getValidMoves(2);
  if (!blackMoves.length && !whiteMoves.length) {
    const black = board.flat().filter(v => v === 1).length;
    const white = board.flat().filter(v => v === 2).length;
    if (black > white) statusP.textContent = '黒の勝ち';
    else if (white > black) statusP.textContent = '白の勝ち';
    else statusP.textContent = '引き分け';
    return true;
  }
  if (!blackMoves.length) {
    statusP.textContent = '黒は置けません。白の番です。';
    aiMove();
    drawBoard();
    return checkGameEnd();
  }
  return false;
}

boardDiv.addEventListener('click', e => {
  const cell = e.target.closest('.cell');
  if (!cell) return;
  const r = parseInt(cell.dataset.row);
  const c = parseInt(cell.dataset.col);
  if (!isValidMove(r, c, 1)) return;
  applyMove(r, c, 1);
  if (getValidMoves(2).length) aiMove();
  drawBoard();
  if (!checkGameEnd()) statusP.textContent = '黒の番です。';
});

drawBoard();
statusP.textContent = '黒の番です。';
