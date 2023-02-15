import tkinter as tk


class State:

    def __init__(self, bar, status, plot, dataframe, quit):
        self.PROCESSING = ProcessingState(self, bar, status, plot, dataframe, quit)
        self.STANBY = StandbyState(self, bar, status, plot, dataframe, quit)
        self.set_state(self.STANBY)

    def set_state(self, state):
        self.state = state

    def start(self):
        """Start the state if it is stopped"""
        self.state.start()

    def stop(self):
        """Stop the state if it is running"""
        self.state.stop()


class ProcessingState:

    def __init__(self, state, bar, status, plot, dataframe, quit):
        self.state = state
        self.bar = bar
        self.status = status
        self.plot = plot
        self.dataframe = dataframe
        self.quit = quit

    def start(self):
        pass

    def stop(self):
        self.state.set_state(self.state.STANBY)
        self.bar.stop()
        self.status.set("Ready")
        self.plot.configure(state=tk.ACTIVE)
        self.dataframe.configure(state=tk.ACTIVE)
        self.quit.configure(state=tk.ACTIVE)
        self.bar.config(value=100)


class StandbyState:

    def __init__(self, state, bar, status, plot, dataframe, quit):
        self.state = state
        self.bar = bar
        self.status = status
        self.plot = plot
        self.dataframe = dataframe
        self.quit = quit

    def start(self):
        self.state.set_state(self.state.PROCESSING)
        self.bar.start(50)

    def stop(self):
        pass
