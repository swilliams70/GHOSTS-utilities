from tkinter import *
from datetime import datetime
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mpd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

# This is based off the excellent examples found here:
#   https://github.com/epogrebnyak/hrange/blob/master/hrange.py
#   https://datatofish.com/matplotlib-charts-tkinter-gui/
#   https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python
# ...any crapulence is my own...

class mclass():
    def __init__(self, window):
        self.window = window
        self.plot()
        #self.button = Button (window, text="check", command=self.plot)
        #self.button.pack()

    def plot(self):
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        j = json.loads(open('test.json').read())
        EvtType = []
        EvtStart = []
        EvtEnd = []

        for x in range(len(j['TimeLineHandlers'])):
            EvtType.append(j['TimeLineHandlers'][x]['HandlerType'])
            EvtStart.append(mpd.date2num(datetime.strptime("{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOn']),"%Y-%m-%d %H:%M:%S")))
            EvtEnd.append(mpd.date2num(datetime.strptime("{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOff']),"%Y-%m-%d %H:%M:%S")))

        vrange = range(len(EvtStart))
        w = [abs(e-s) for s, e in zip(EvtStart, EvtEnd)]
        fig, ax = plt.subplots()
        ax.barh(vrange, width=w, left=EvtStart, height=0.5)
        plt.yticks(vrange, EvtType)

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()        
    
if __name__=="__main__":

    window=Tk()
    start=mclass(window)
    window.mainloop()

