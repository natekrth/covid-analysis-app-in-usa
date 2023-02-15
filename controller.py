class Controller:
    """medium between model and view"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.prepare = None

    def save(self, *args):
        """
        save data for preparing.
        """
        timeframe_sort = args[0]
        state_sort = args[1]
        topic_sort = args[2]
        selected = args[3]

        if selected == '1':
            self.prepare = self.model.prepare_data1(state_sort, topic_sort, timeframe_sort)
            self.view.plot_1(self.prepare)
        elif selected == '2':
            self.prepare = self.model.prepare_data2(state_sort, topic_sort, timeframe_sort)
            self.view.plot_2(self.prepare)

    def save_sort(self, state):
        self.prepare = self.model.prepare_state_sort(state)
        self.view.update_treeview(self.prepare)
