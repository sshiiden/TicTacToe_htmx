from flask import Flask, render_template

app = Flask(__name__)

class Board:
    def __init__(self) -> None:
        self.turn = "X"
        self.board = ["" for _ in range(9)]
        self.winner = ""

    def move(self, cell):
        if not self.winner:
            self.board[cell] = self.turn 
            self.turn = "X" if self.turn == "O" else "O"

    def new_game(self):
        self.__init__()

    def check_winner(self):
        lines = ((0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6))
        for i in range(len(lines)):
            a, b, c = lines[i]
            if self.board[a] and self.board[a] == self.board[b] and self.board[a] == self.board[c]:
                self.winner = self.board[a]

    def check_draw(self):
        if not "" in self.board:
            self.winner = "draw"
            return True

game = Board()

@app.route("/")
def index():
    return render_template("index.html", game=game, status=status)

@app.route("/move/<int:cell>")
def move(cell):
    game.move(cell)
    return f'<button class="cell">{ game.board[cell] }</button>'

@app.route("/status")
def status():
    game.check_winner()
    if game.check_draw():
        return "Draw."
    elif game.winner:
        return f"{game.winner} won."
    else:
        return f"It's {game.turn} turn."

@app.route("/new_game")
def new_game():
    game.new_game()
    return render_template("board.html", game=game, status=status)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)