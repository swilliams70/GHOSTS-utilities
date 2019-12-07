#we declare needed libraries
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter.ttk import *
from PIL import Image, ImageTk
import ruamel.yaml as yaml
import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mpd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
#import dateutil

#Create a class for the window you're going to create.
class TLEditor(Tk):

    #Just init stuff, pretty boilerplate.
    def __init__(self):
        Tk.__init__(self)

        #window title and style stuff
        self.title("Timeline Author")
        #geometry is "window width x window height + position x + position y"
        self.geometry("1200x600+200+50")
        self.style = Style()
        self.style.theme_use("default")

        #Create menus
        menubar = Menu(self.master)
        self.config(menu = menubar)
        fileMenu = Menu(menubar)
        menubar.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label="New", command = self.newFile)
        #FIX THIS: open appends when there is already a timeline open!!!
        fileMenu.add_command(label="Open", command = self.openFile)
        fileMenu.add_command(label="Save", command = self.saveFile)
        fileMenu.add_separator()
        fileMenu.add_command(label = "Exit", command = self.onExit)



        #create a frame for editor
        self.editorFrame = Frame(self)
        self.editorFrame.place(relx = 0, rely = 0, relwidth = .33, relheight = 1)

        self.labelEditor = Label(self.editorFrame, text = "Editor", width = 6)
        self.labelEditor.pack(side = TOP, padx = 5, pady = 5)

        self.frameEditor = scrolledtext.ScrolledText(self.editorFrame)
        self.frameEditor.pack(fill = BOTH, padx = 5, pady = 5, expand = True)

        #create a frame for parser
        self.parserFrame = Frame(self)
        self.parserFrame.place(relx = .33, rely = 0, relwidth = .75, relheight = 1)

        #self.labelParser = Label(self.parserFrame, text = "Parser", width = 6)
        #self.labelParser.pack(side = TOP, padx = 5, pady = 5)

        self.createPlot()


    def createPlot(self):
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')

        dates = []

        datestrings = ['00:00:00', '04:00:00', '08:00:00', '12:00:00', '16:00:00', '20:00:00', '23:59:59']
        for d in range(len(datestrings)):
            dates.append(mpd.date2num(datetime.strptime("{} {}".format(today_str, datestrings[d]),"%Y-%m-%d %H:%M:%S")))
        #times = [dateutil.parser.parse(d) for d in datestrings]

        fig = plt.figure()

        plt_data = [0,len(datestrings)]
        plt.yticks(plt_data)
        plt.xlim(dates[0], dates[len(datestrings)-1])
        plt.xticks(rotation = 25 )
        plt.subplots_adjust(bottom = .2)

        #create xaxis formatted to time
        ax=plt.gca()
        xfmt = mpd.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        ax.set_xticks(dates)

        canvas=FigureCanvasTkAgg(fig,master = self.parserFrame)
        canvas.get_tk_widget().grid(row = 0, column = 1)
        canvas.draw()

        self.plotbutton = Button(master = self.parserFrame, text="plot", command=lambda: self.new_plot(canvas,ax))
        self.plotbutton.grid(row = 0, column = 0)

    def new_plot(self, canvas, ax):

        ax.clear()

        EvtType = []
        EvtStart = []
        EvtEnd = []

        j = json.loads(open('test.json').read())

        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')


        for x in range(len(j['TimeLineHandlers'])):
            EvtType.append(j['TimeLineHandlers'][x]['HandlerType'])
            EvtStart.append(mpd.date2num(datetime.strptime("{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOn']),"%Y-%m-%d %H:%M:%S")))
            EvtEnd.append(mpd.date2num(datetime.strptime("{} {}".format(today_str, j['TimeLineHandlers'][x]['UtcTimeOff']),"%Y-%m-%d %H:%M:%S")))

        vrange = range(len(EvtStart))
        w = [abs(e-s) for s, e in zip(EvtStart, EvtEnd)]

        fig, ax = plt.subplots()

        xfmt = mpd.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)

        ax.barh(vrange, width = w, left = EvtStart, height = 0.5)
        ax.xaxis_date()

        plt.xticks( rotation=25 )
        plt.yticks(vrange, EvtType)

        #appear to NEED this part to display, but won't update
        canvas=FigureCanvasTkAgg(fig,master = self.parserFrame)
        canvas.get_tk_widget().grid(row = 0, column = 1)
        canvas.draw()



    def old_plot(self, j):

        ax.clear()

        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        #j = json.loads(open('test.json').read())
        #print(j)
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

        xfmt = mpd.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)

        ax.barh(vrange, width = w, left = EvtStart, height = 0.5)
        ax.xaxis_date()

        plt.xticks( rotation=25 )
        plt.yticks(vrange, EvtType)

        #appear to NEED this part to display, but won't update
        canvas=FigureCanvasTkAgg(fig,master = self.parserFrame)
        canvas.get_tk_widget().grid(row = 0, column = 1)
        canvas.draw()


    def newFile(self):
        if len(self.frameEditor.get('1.0', END+'-1c')) > 0:
            if messagebox.askyesno("Save?", "Do you want to save?"):
                saveFile()
            else:
                self.frameEditor.delete('1.0', END)

                            
    def openFile(self):
        file = filedialog.askopenfile(parent=self, mode='r', title='Select a file')

        if file != None:
            if len(self.frameEditor.get('1.0', END+'-1c')) > 0:
                if messagebox.askyesno("Save?", "Do you want to save?"):
                    saveFile()
                else:
                    self.frameEditor.delete('1.0', END)
                    json_object = json.loads(file.read())
                    self.yaml_string = yaml.dump(json_object, indent=2, default_flow_style=False)
                    self.frameEditor.insert('1.0', self.yaml_string)
                    file.close()
                    self.old_plot(json_object)
                    #self.plot(canvas, ax)
            else:
                json_object = json.loads(file.read())
                self.yaml_string = yaml.dump(json_object, indent=2, default_flow_style=False)
                self.frameEditor.insert('1.0', self.yaml_string)
                file.close()
                self.old_plot(json_object)
                #self.plot(self.canvas, self.ax)

    def saveFile(self):
        file = filedialog.asksaveasfile(mode='w')

        if file != None:
            #drop extra return at the end
            yaml_object = yaml.load(self.frameEditor.get('1.0', END+'-1c')) 
            self.json_string = json.dumps(yaml_object, indent=4, sort_keys=False)
            file.write(self.json_string)
            file.close()

    def onExit(self):
        if messagebox.askyesno("Quit", "Are you sure?"):
            self.destroy()        

    def resize(self, event):
        size = (event.width, event.height)
        resized = self.original.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image = self.image, anchor = NW, tags = "IMG")



#the guts of our application invoked from here
def main():
        
    #create an instance of the editor
    app = TLEditor()
    
    #builtin tkinter mainloop to handle all the windowy stuff
    app.mainloop()

#when run, do the main function, pretty standard
if __name__=='__main__':
    main()
