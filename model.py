import pandas as pd


class Model:

    def __init__(self, covid):
        self._covid = pd.read_csv(covid, index_col='date', parse_dates=[0])
        self.reset_covid = self._covid.reset_index()
        self.reset_covid["date"] = pd.to_datetime(self.reset_covid["date"]).dt.date

    def prepare_data1(self, state, topic, timeframe):
        """
        prepare data for the left graph plot.
        :param state: value from state combobox
        :param topic: value from topic combobox
        :param timeframe: value from timeframe combobox
        :return: dataframe
        """
        covid = self._covid
        covid_topic = covid[covid.state == state][topic].resample(timeframe).sum()
        return covid_topic

    def prepare_data2(self, state, topic, timeframe):
        """
        prepare data for the right graph plot.
        :param state: value from state combobox
        :param topic: value from topic combobox
        :param timeframe: value from timeframe combobox
        :return: dataframe
        """
        covid = self._covid
        covid_topic2 = covid[covid.state == state][topic].resample(timeframe).sum()
        return covid_topic2

    def prepare_state_sort(self, state):
        return self.reset_covid[self.reset_covid.state == state]
