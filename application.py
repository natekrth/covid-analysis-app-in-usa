import tkinter as tk
from model import Model
from view import View
from controller import Controller


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('USA Covid-19 Analysis App')
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.minsize(width=1280, height=800)
        self.maxsize(width=self.width, height=self.height)

        # create a model.
        model = Model("all-states-history.csv")

        # create a view and place it on the root window.
        view = View(self)
        view.grid(row=0, column=0)

        # create a controller.
        controller = Controller(model, view)

        # set the controller to view.
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()
