import json
import sys
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi
import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QPixmap, QImage
import calendar
from datetime import datetime,date

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import get_T_info

now = datetime.now()
x=calendar.day_name[date.today().weekday()]
x=x[0:3]

week = (now.day + 6 - now.weekday()) // 7
if week==0:
    week=1
week='week'+str(week)

month_name=datetime.now().strftime('%B')

class LogScreen(QDialog):
    def __init__(self,name):
        super(LogScreen, self).__init__()
        loadUi("Screens/dialog.ui",self)
        self.name = str(name)
        self.plot_weekly_graph(name)
        # self.YearlyGraph(name)
        self.btnweek.clicked.connect(self.setPixmap)
        self.btnyear.clicked.connect(self.setPixmap1)
        self.todays.setText(calendar.day_name[date.today().weekday()])
        dc=get_T_info.getValue(name,month_name,week,x)[0]
        wc=str(get_T_info.getValue(name,month_name,week,x)[1])
        self.dailycount.setText(dc)
        self.weeklycount.setText(wc)

        # self.graph.setPixmap(QPixmap(self.name+'image.png'))


    def plot_weekly_graph(self, name):
        with open('Json/weekly.json') as f:
            data = json.load(f)
        data = data[name]
        month_name = datetime.now().strftime('%B')

        # Generate the x-axis labels for the monthly graph
        month_labels = []
        for i in range(1, 5):
            for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                month_labels.append(day)

        # Generate the y-axis data for the monthly graph
        monthly_data = []
        for i in range(1, 5):
            week_data = []
            for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
                try:
                    week_data.append(data[month_name][f'week{i}'][day])
                except KeyError:
                    week_data.append(None)
            monthly_data.append(week_data)

        # Set up the plot
        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot the monthly data as a spline chart
        x = np.arange(len(month_labels))

        week_colors = ['red', 'blue', 'green', 'orange']

        for i in range(len(monthly_data)):
            if all(d is None for d in monthly_data[i]):  # skip empty weeks
                continue
            ax.plot(x[7 * i:7 * (i + 1)], monthly_data[i], '-o', label=f'Week {i + 1}', color=week_colors[i], markersize=3)
            for j, y in enumerate(monthly_data[i]):
                if y is not None:  # skip None values
                    ax.annotate(f'{month_labels[7 * i + j]}', xy=(x[7 * i + j], y), xytext=(x[7 * i + j], y + 0.1), ha='right',
                                fontsize=10)
        ax.set_xlabel('Day of Month')
        ax.set_ylabel('Number of Biting Attempts')
        ax.set_xticks(x[3::7])
        ax.set_xticklabels(['Week 1', 'Week 2', 'Week 3', 'Week 4'])
        ax.set_title('Monthly Biting Attempts')
        ax.legend()
        canvas = FigureCanvasQTAgg(fig)
        canvas.draw()

        # Convert the canvas buffer to QImage
        buffer = canvas.buffer_rgba()
        width, height = buffer.shape[1], buffer.shape[0]
        image = QImage(buffer.tobytes(), width, height, QImage.Format_RGBA8888)

        # Convert QImage to QPixmap and set it to QLabel
        pixmap = QPixmap.fromImage(image)
        self.graph.setPixmap(pixmap)


    def YearlyGraph(self,name):

        with open('Json/yearly.json') as f:
            data = json.load(f)
        data = data[name]
        # Generate the x-axis labels for the yearly graph
        month_labels = list(data['yearly'].keys())

        # Generate the y-axis data for the yearly graph
        yearly_data = list(data['yearly'].values())

        # Set up the plot
        # sc = MplCanvas(self, width=8, height=4, dpi=90)
        # ax = sc.axes
        fig, ax = plt.subplots(figsize=(8, 5))

        # Check if all monthly data is present in the JSON file
        if all(month in data['yearly'] for month in month_labels):
            # Plot the yearly data as a bar chart
            x = range(len(month_labels))
            ax.bar(x, yearly_data, align='center', alpha=0.5, color='blue')

            # Add text to the top of each bar
            for i, val in enumerate(yearly_data):
                ax.text(i, val, str(val), ha='center', va='bottom', fontsize=10)

            ax.set_facecolor('white')
            ax.set_xticks(x)
            ax.set_xticklabels(month_labels)
            ax.tick_params(axis='x', labelsize=7)
            ax.set_xlabel('Yearly')
            ax.set_ylabel('Number of Biting Attempts')
            ax.set_title('Yearly Biting Attempts')

        else:
            print("Some monthly data is missing from the JSON file.")

        canvas = FigureCanvasQTAgg(fig)
        canvas.draw()

        # Convert the canvas buffer to QImage
        buffer = canvas.buffer_rgba()
        width, height = buffer.shape[1], buffer.shape[0]
        image = QImage(buffer.tobytes(), width, height, QImage.Format_RGBA8888)

        # Convert QImage to QPixmap and set it to QLabel
        pixmap = QPixmap.fromImage(image)
        self.graph.setPixmap(pixmap)


    def setPixmap(self,name):
        self.plot_weekly_graph(self.name)
        plt.close()
        print("Button 1 is being run")


    def setPixmap1(self):
        self.YearlyGraph(self.name)
        plt.close()
        print("Button 2 is being run")



if __name__=='__main__':

    app = QApplication(sys.argv)
    window=LogScreen()
    window.setFixedSize(1150,850)
    window.show()
    app.exec()
