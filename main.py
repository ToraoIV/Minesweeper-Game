import customtkinter as ctk
import random
from tkinter import messagebox

root = ctk.CTk()
root.title("Minesweeper")
root.geometry("480x480")
root.resizable(False, False)


class Cell:
    all = []
    def __init__(self, x, y, mine=False):
        self.mine = mine
        self.btn_object = None
        self.x = x
        self.y = y
        self.candidate = False

        Cell.all.append(self)

    def create_button(self, location):
        btn = ctk.CTkButton(
            location,
            height=60,
            width=60,
            corner_radius=0,
            text="",
            border_width = 1,
            fg_color = "#1f1f1f",
            hover_color = "#5c5b5b"
        )
        self.btn_object = btn
        btn.bind("<Button-1>", self.left_click)
        btn.bind("<Button-3>", self.right_click)

    def left_click(self, event):
        if self.mine:
            self.show_mine()
        else:
            if self.lenght() == 0:
                for cell_obj in self.surrounded:
                    cell_obj.show_cell()

            self.show_cell()
        self.btn_object.unbind("<Button-1>")
        self.btn_object.unbind("<Button-3>")

    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded(self):
        surrounded_cells = [
            self.get_cell(self.x - 1, self.y - 1),
            self.get_cell(self.x - 1, self.y),
            self.get_cell(self.x - 1, self.y + 1),
            self.get_cell(self.x, self.y - 1),
            self.get_cell(self.x + 1, self.y - 1),
            self.get_cell(self.x + 1, self.y),
            self.get_cell(self.x + 1, self.y + 1),
            self.get_cell(self.x, self.y + 1)
        ]

        surrounded_cells = [cell for cell in surrounded_cells if cell is not None]
        return surrounded_cells

    def right_click(self, event):
        if not self.candidate:
            self.btn_object.configure(fg_color="orange")
            self.candidate = True
        else:
            self.btn_object.configure(fg_color="blue")
            self.candidate = False

    def lenght(self):
        counter = 0
        for cell in self.surrounded:
            if cell.mine:
                counter += 1

        return counter

    def show_cell(self):
        self.btn_object.configure(text=self.lenght())

    def show_mine(self):
        self.btn_object.configure(fg_color="red")
        messagebox.showerror('Game Over', 'You Lose!')

    @staticmethod
    def random_mines():
        picked_cells = random.sample(Cell.all, 15)

        for picked in picked_cells:
            picked.mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


for x in range(8):
    for y in range(8):
        c = Cell(x, y)
        c.create_button(root)
        c.btn_object.grid(column=x, row=y)

Cell.random_mines()

root.mainloop()
