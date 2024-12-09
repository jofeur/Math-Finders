import tkinter as tk
import random
from graph import Maze
from linkedList import MathLinkedList
from stacks import PlayerStack
from hashTable import ProficiencyHashTable
from tree import GameTree


class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Finders")

        self.canvas = tk.Canvas(root, width=600, height=600, bg="lightblue")
        self.canvas.pack()

        self.cell_size = 60
        self.player_color = "red"
        self.target_color = "green"

        self.math_problems = MathLinkedList()
        self.populate_math_problems()

        self.wrong_answers_stack = PlayerStack()

        self.proficiency_table = ProficiencyHashTable()

        self.game_tree = GameTree()
        self.current_level_node = self.game_tree.root

        self.start_level()

        self.root.bind("<Up>", self.attempt_move_up)
        self.root.bind("<Down>", self.attempt_move_down)
        self.root.bind("<Left>", self.attempt_move_left)
        self.root.bind("<Right>", self.attempt_move_right)

    def show_message(self, title, message, color="lightgreen"):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.configure(bg=color)

        tk.Label(dialog, text=message, bg=color, fg="black", font=("Comic Sans MS", 14)).pack(pady=20)
        tk.Button(dialog, text="OK", command=dialog.destroy, bg="white", fg="black").pack(pady=10)

    def ask_integer(self, title, question, color="lightblue"):
        result = tk.IntVar()  
        result.set(None) 

        def submit():
            try:
                user_input = int(entry.get())
                result.set(user_input)
                dialog.destroy()
            except ValueError:
                error_label.config(text="Please enter a valid number", fg="red")

        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.configure(bg=color)

        tk.Label(dialog, text=question, bg=color, font=("Comic Sans MS", 14)).pack(pady=10)
        entry = tk.Entry(dialog, font=("Comic Sans MS", 14))
        entry.pack(pady=5)
        error_label = tk.Label(dialog, bg=color, font=("Comic Sans MS", 12))
        error_label.pack()

        tk.Button(dialog, text="Submit", command=submit, bg="white", fg="black").pack(pady=10)
        dialog.grab_set()  

        self.root.wait_window(dialog)
        return result.get()

    def start_level(self):
        self.show_message(
            "Level Start",
            f"Welcome to {self.current_level_node.description}\n"
            f"Difficulty: {self.current_level_node.difficulty}",
        )

        self.maze = Maze().get_maze(self.current_level_node.level_number)
        self.player_position = [1, 1]
        self.target_position = [8, 8]
        self.canvas.delete("all")
        self.draw_maze()
        self.player = self.draw_player(*self.player_position)

    def draw_maze(self):
        orange = ["orange"]
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze[row][col] == 1:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=random.choice(orange)
                    )
                elif [row, col] == self.target_position:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.target_color, outline="white"
                    )

    def draw_player(self, row, col):
        x1 = col * self.cell_size + 10
        y1 = row * self.cell_size + 10
        x2 = x1 + self.cell_size - 20
        y2 = y1 + self.cell_size - 20
        return self.canvas.create_oval(x1, y1, x2, y2, fill=self.player_color)

    def move_player(self, row, col):
        if 0 <= row < len(self.maze) and 0 <= col < len(self.maze[0]) and self.maze[row][col] == 0:
            self.player_position = [row, col]
            self.canvas.delete(self.player)
            self.player = self.draw_player(row, col)

            if self.player_position == self.target_position:
                self.win_level()

    def attempt_move(self, row_offset, col_offset):
        if self.ask_math_question():
            new_row = self.player_position[0] + row_offset
            new_col = self.player_position[1] + col_offset
            self.move_player(new_row, new_col)

    def attempt_move_up(self, event):
        self.attempt_move(-1, 0)

    def attempt_move_down(self, event):
        self.attempt_move(1, 0)

    def attempt_move_left(self, event):
        self.attempt_move(0, -1)

    def attempt_move_right(self, event):
        self.attempt_move(0, 1)

    def ask_math_question(self):
        problem, solution = self.math_problems.get_problem()
        if not problem:
            self.show_message("You've answered all the questions")
            return True

        user_answer = self.ask_integer("Math Question", f"Solve: {problem}")
        if user_answer == solution:
            self.show_message("Correct", "That is Correct Great job!", color="lightgreen")
            return True
        else:
            self.show_message("Incorrect", "That's not correct. Try again", color="red")
            self.wrong_answers_stack.push(problem, solution)
            return False

    def populate_math_problems(self):
        for _ in range(100):
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            operation = random.choice(["+", "-"])
            if num1 < num2:
                problem = f"{num2} {operation} {num1}"
            else:    
                 problem = f"{num1} {operation} {num2}"
            solution = eval(problem)
            self.math_problems.add_problem(problem, solution)

    def win_level(self):
        if self.current_level_node.children:
            self.show_message(
                "Level Complete",
                f"Congratulations! You've completed {self.current_level_node.description}.",
            )
            self.current_level_node = self.current_level_node.children[0]
            self.start_level()
        else:
            self.finish_game()

    def finish_game(self):
        total_wrong_answers = self.wrong_answers_stack.size()
        player_name = self.ask_integer("Please enter your name:")

        self.proficiency_table.add_player(player_name, total_wrong_answers)
        proficiency = self.proficiency_table.get_player_proficiency(player_name)

        wrong_answers = []
        while not self.wrong_answers_stack.is_empty():
            problem, solution = self.wrong_answers_stack.pop()
            wrong_answers.append(f"{problem} = {solution}")

        self.show_message(
            "Game Over",
            f"Congratulations {player_name}! Your proficiency level is: {proficiency}\n"
            f"Incorrect answers:\n" + "\n".join(wrong_answers),
            color="lightblue",
        )

        self.canvas.create_text(
            300,
            300,
            text=f" You Win the Game! \nProficiency: {proficiency}",
            font=("Comic Sans MS", 24),
            fill="purple",
        )
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")


if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()