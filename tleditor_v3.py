from tkinter import Tk, scrolledtext, Menu, filedialog, END, messagebox
import ruamel.yaml as yaml
import json

#root class for main window
root = Tk(className = "Text Editor")
textArea = scrolledtext.ScrolledText(root, width=100, height=50)

#Functions
def newFile():
    if len(textArea.get('1.0', END+'-1c')) > 0:
        if messagebox.askyesno("Save?", "Do you want to save?"):
            saveFile()
        else:
            textArea.delete('1.0', END)

                        
def openFile():
    file = filedialog.askopenfile(parent=root, mode='r', title='Select a file')

    if file != None:
        json_object = json.loads(file.read())
        textArea.insert('1.0', yaml.dump(json_object, indent=2, default_flow_style=False)) #yaml.dump reorders dict
        file.close()

def saveFile():
    file = filedialog.asksaveasfile(mode='w')

    if file != None:
        yaml_object = yaml.load(textArea.get('1.0', END+'-1c')) #drop extra return at the end
        file.write(json.dumps(yaml_object, indent=4, sort_keys=False))
        file.close()

def about():
    label = messagebox.showinfo("About", "simple editor")

def exitRoot():
    if messagebox.askyesno("Quit", "Are you sure?"):
        root.destroy()


#create menus
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command =exitRoot)


helpMenu = Menu(menu)
menu.add_cascade(label="Help")
menu.add_cascade(label="About", command=about)

textArea.pack()

#main loop
root.mainloop()







