import pandas as pd
import tkinter as tk
from tkintermapview import TkinterMapView
import customtkinter
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from threading import Thread
from state import State


class View(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.covid = pd.read_csv("all-states-history.csv", index_col='date', parse_dates=[0])
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.selected = tk.StringVar()
        self.selected.set('1')
        self.status = tk.StringVar()
        self.status.set("Ready")
        self.load = tk.StringVar()
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """create initial widgets and frames on the screen."""

        # title
        title_label = ttk.Label(self, text='USA Covid-19 Analysis', font=("Monospace", 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NS)

        self.quit_button = ttk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=0, column=0, sticky=tk.NW)
        # showing dataframe
        self.show_data = ttk.Treeview(self)
        self.show_data.grid(row=1, column=0, columnspan=2)

        # put data into treeview
        self.update_treeview(self.covid)

        # create scrollbar for treeview
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.show_data.xview)
        self.show_data.configure(xscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='NSE')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create first figure canvas for plot
        self.fig_canvas1 = Figure()
        self.axes1 = self.fig_canvas1.add_subplot()
        self.fig_canvas1.subplots_adjust(left=0.3, bottom=0.2)
        self.fig_canvas1 = FigureCanvasTkAgg(self.fig_canvas1, master=self)
        self.fig_canvas1.get_tk_widget().grid(row=2, column=0, sticky="NEWS", padx=10, pady=20)

        # create second figure canvas for plot
        self.fig_canvas2 = Figure()
        self.axes2 = self.fig_canvas2.add_subplot()
        self.fig_canvas2.subplots_adjust(left=0.3, bottom=0.2)
        self.fig_canvas2 = FigureCanvasTkAgg(self.fig_canvas2, master=self)
        self.fig_canvas2.get_tk_widget().grid(row=2, column=1, sticky="NEWS", padx=10, pady=20)

        # create sort_frame
        self.sort_frame = ttk.LabelFrame(self, text="Select Sort")
        self.sort_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="NEWS")

        # create label for selecting plot graph
        select_plot_label = ttk.Label(self.sort_frame, text="Select Graph")
        select_plot_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky='N')

        # create radiobutton for selecting plot graph
        self.select_plot1 = ttk.Radiobutton(self.sort_frame, text="1", value='1', variable=self.selected)
        self.select_plot1.grid(row=1, column=0, padx=20, pady=10, sticky='N')
        self.select_plot2 = ttk.Radiobutton(self.sort_frame, text="2", value='2', variable=self.selected)
        self.select_plot2.grid(row=1, column=1, padx=20, pady=10, sticky='N')

        # create label and combobox for timeframe sorting
        timeframe_label = ttk.Label(self.sort_frame, text='Timeframe')
        timeframe_label.grid(row=2, column=0, pady=10)
        self.timeframe = ttk.Combobox(self.sort_frame, state="readonly")
        self.timeframe.grid(row=3, column=0, padx=20, pady=10, sticky='NEWS')
        self.timeframe.config(values=["D", "M", "Y"])
        self.timeframe.current(1)

        # create label and combobox for state sorting
        state_label = ttk.Label(self.sort_frame, text="State")
        state_label.grid(row=2, column=1, padx=20, pady=10)
        self.state = ttk.Combobox(self.sort_frame, state="readonly")
        self.state.grid(row=3, column=1, padx=20, pady=10, sticky='NEWS')
        self.state.config(values=list(self.covid.state.unique()))
        self.state.current(0)

        # create label and combobox for topic sorting
        topic_label = ttk.Label(self.sort_frame, text="Topic")
        topic_label.grid(row=4, column=0)
        self.topic = ttk.Combobox(self.sort_frame, state="readonly")
        self.topic.grid(row=5, column=0, padx=20, pady=10, sticky='NEWS')
        self.topic.config(values=list(self.covid.columns))
        self.topic.current(1)

        # create label and combobox for selecting plot type
        plot_type_label = ttk.Label(self.sort_frame, text='Plot Type')
        plot_type_label.grid(row=4, column=1, pady=10)
        self.plot_type = ttk.Combobox(self.sort_frame, state="readonly")
        self.plot_type.bind('<<ComboboxSelected>>', self.update_timeframe)
        self.plot_type.grid(row=5, column=1, padx=20, pady=10, sticky='NEWS')
        self.plot_type.config(values=["barh", "line", "hist"])
        self.plot_type.current(2)

        # create plot button
        self.plot_button = ttk.Button(self.sort_frame, text="Plot", command=self.plot_button_clicked)
        self.plot_button.grid(row=5, column=2, sticky='W')

        # create sorting by state button
        self.dataframe_button = self.clear_button = ttk.Button(self.sort_frame, text="Sort by state",
                                                               command=self.sort_state_clicked)
        self.dataframe_button.grid(row=5, column=2)

        # create clear button for clearing plot graph
        self.clear_button = ttk.Button(self.sort_frame, text="Clear", command=self.clear_button_clicked)
        self.clear_button.grid(row=5, column=2, sticky='E')

        # create another frame for progressbar
        self.frame1 = ttk.LabelFrame(self.sort_frame, text="Status")
        self.frame1.grid(row=4, column=2, sticky="NEWS", padx=10, pady=10)
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)

        # create label and progressbar
        self.status_label = ttk.Label(self.frame1, textvariable=self.status)
        self.status_label.grid(row=0, column=0, sticky="NEWS", padx=10)
        self.bar1 = ttk.Progressbar(self.frame1, length=500, mode="determinate")
        self.bar1.grid(row=1, column=0, sticky="NEWS", padx=10)

        (sort_frame_cols, sort_frame_rows) = self.sort_frame.grid_size()
        for col in range(sort_frame_cols):
            self.sort_frame.columnconfigure(col, weight=1)
        for row in range(sort_frame_rows):
            self.sort_frame.rowconfigure(row, weight=1)

        # create another frame for a map
        self.frame_right = customtkinter.CTkFrame(self.sort_frame, corner_radius=10)
        self.frame_right.grid(row=0, column=2, rowspan=4, pady=10, padx=10, sticky="NEWS")

        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(2, weight=1)

        # create a map using tkintermapview
        self.map_widget = TkinterMapView(self.frame_right, width=250, height=150, corner_radius=9)
        self.map_widget.grid(row=0, rowspan=1, column=0, columnspan=3, sticky="NEWS", padx=10, pady=10)
        self.map_widget.set_address(self.state.get())
        self.map_widget.set_zoom(5)

        # create label beside map
        self.label = customtkinter.CTkLabel(master=self.frame_right,
                                            text=f"State : {self.state.get()}",
                                            width=140,
                                            height=30,
                                            corner_radius=8)
        self.label.grid(row=1, column=0, sticky="NEWS", padx=10, pady=10)

    def plot_button_clicked(self):
        """event after plot button has been clicked"""
        self.plot_button.configure(state=tk.DISABLED)
        self.dataframe_button.configure(state=tk.DISABLED)
        self.quit_button.configure(state=tk.DISABLED)
        self.run_task(self.plotting)

    def sort_state_clicked(self):
        """event after sorting by state button has been clicked"""
        self.plot_button.configure(state=tk.DISABLED)
        self.dataframe_button.configure(state=tk.DISABLED)
        self.quit_button.configure(state=tk.DISABLED)
        self.run_task(self.sorting)

    def update_timeframe(self, take):
        """update value inside timeframe combobox"""
        if self.plot_type.get() == "line" or self.plot_type.get() == "barh":
            self.timeframe.set("M")
            self.timeframe.config(values=["M", "Y"])
        else:
            self.timeframe.config(values=["D", "M", "Y"])

    def update_treeview(self, data):
        """update treeview value in both rows and columns"""
        covid_data = data

        for i in self.show_data.get_children():
            self.show_data.delete(i)

        index_reset = covid_data.reset_index()
        self.show_data['column'] = list(index_reset.columns)
        self.show_data['show'] = "headings"

        for column in self.show_data['column']:
            self.show_data.heading(column, text=column)

        row_data = index_reset.to_numpy().tolist()
        for row in row_data:
            self.show_data.insert("", "end", text=index_reset.index, values=row)

    def run_task(self, task):
        self.task_thread = Thread(target=task)
        self.task_thread.start()
        self.states = State(self.bar1, self.status, self.plot_button, self.dataframe_button, self.quit_button)
        self.states.start()

    def plotting(self):
        """plotting task"""
        self.status.set("Plotting...")
        self.map_widget.set_address(f"{self.state.get()} USA")
        self.map_widget.set_zoom(5)
        self.controller.save(self.timeframe.get(), self.state.get(), self.topic.get(), self.selected.get())
        self.label['text'] = f"State : {self.state.get()}"
        self.states.stop()

    def sorting(self):
        """sorting task."""
        self.status.set("Sorting...")
        self.map_widget.set_address(f"{self.state.get()} USA")
        self.map_widget.set_zoom(5)
        self.controller.save_sort(self.state.get())
        self.states.stop()

    def clear_button_clicked(self):
        """event after clear button has been clicked."""
        if self.selected.get() == '1':
            self.axes1.clear()
            self.fig_canvas1.draw()
        elif self.selected.get() == '2':
            self.axes2.clear()
            self.fig_canvas2.draw()

    def plot_1(self, data1):
        """Plot left graph"""
        self.update_treeview(data1)
        self.axes1.clear()
        data1.plot(ax=self.axes1, kind=f"{self.plot_type.get()}", title=f"{self.topic.get()} in {self.state.get()}",
                   xlabel=self.timeframe.get(), ylabel=self.topic.get(),
                   legend=True, grid=True)
        self.fig_canvas1.draw()

    def plot_2(self, data2):
        """Plot right graph"""
        self.update_treeview(data2)
        self.axes2.clear()
        data2.plot(ax=self.axes2, kind=f"{self.plot_type.get()}", title=f"{self.topic.get()} in {self.state.get()}",
                   xlabel=self.timeframe.get(), ylabel=self.topic.get(),
                   legend=True, grid=True)
        self.fig_canvas2.draw()

    def set_controller(self, controller):
        """Set the controller"""
        self.controller = controller
