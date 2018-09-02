import tkinter as tk
from tkinter import filedialog as fd
import tkinter.simpledialog as tksd
import cbtl_base as tlbase
import cbtl_tween as tween
import cbtl_video as video
from PIL import Image,ImageTk
import math

class Application(tk.Frame):
    def __init__(self,tl, master=None):
        super().__init__(master)
        self.tl = tl
        #self.pack()
        self.grid()
        self.imgs = []
        self.active = None
        self.n = []
        self.newactiveimage = None
        self.tlimgs = []
        self.create_widgets()
        self.setActive(0)
        

    def create_widgets(self):
        self.toolbarf = tk.Frame(self,bg="black",width=100,height=100)
        self.toolbarc = tk.Canvas(self.toolbarf,width=50, height=50)
        self.toolbarf.grid(row=0,column=0,sticky="e")
        self.toolbarc.pack(side="left")
        self.toolbar = []
        
        self.quit = tk.Button(self.toolbarc, text="QUIT", fg="red",command=root.destroy)
        self.toolbar.append(self.toolbarc.create_window(0,0,anchor="nw",window = self.quit))
        self.quit.pack(side="left")

        self.replaceb = tk.Button(self.toolbarc, text="REPLACE", fg="red",command=self.replace)
        self.toolbar.append(self.toolbarc.create_window(0,0,anchor="nw",window = self.replaceb))
        self.replaceb.pack(side="left")

        self.inserttest = tk.Button(self.toolbarc, text="INSERT", fg="red",command=self.insert)
        self.toolbar.append(self.toolbarc.create_window(0,50,anchor="nw",window = self.inserttest))
        self.inserttest.pack(side="left")

        self.delframe = tk.Button(self.toolbarc, text="DELETE", fg="red",command=self.delete)
        self.toolbar.append(self.toolbarc.create_window(0,50,anchor="nw",window = self.delframe))
        self.delframe.pack(side="left")

        self.load = tk.Button(self.toolbarc, text="LOAD", fg="red",command=self.loadFromFile)
        self.toolbar.append(self.toolbarc.create_window(0,0,anchor="nw",window = self.load))
        self.load.pack(side="left")

        self.saveb = tk.Button(self.toolbarc, text="SAVE", fg="red",command=self.save)
        self.toolbar.append(self.toolbarc.create_window(0,0,anchor="nw",window = self.saveb))
        self.saveb.pack(side="left")
        
        self.renderb = tk.Button(self.toolbarc, text="RENDER", fg="red",command=self.render)
        self.toolbar.append(self.toolbarc.create_window(0,50,anchor="nw",window = self.renderb))
        self.renderb.pack(side="left")
        
        self.update_tl()
 #       tk.after(30, self.update_tl())

    def update_tl(self):
        i=0
        self.thumbs = self.tl.genThumb()
        self.tlimgs = []
        self.imgs = []
        self.acf = tk.Frame(self,bg="black",width=100,height=100)
        self.acf.grid(row=6,column=0)
        self.tlf = tk.Frame(self,bg="red",width=100,height=100)
        
        self.c = tk.Canvas(self.acf,width=600, height=300)
        self.c.pack()
        self.t = tk.Canvas(self.tlf,width=800, height=300)
        self.t.pack()
        self.tlbuttons = []
        for t in self.thumbs:
            self.tlimgs.append(ImageTk.PhotoImage(t))
            tlimg = {}
            tlimg["index"] = i
            tlimg["button"] = tk.Button(self.t,image = self.tlimgs[i],text = str(i),borderwidth=0)#,command = lambda: self.setActive(self.tlimg["index"])) #tk.Label(self,image = self.tlimgs[i])
            self.imgs.append(tlimg)
            i+=1
        self.tlf.grid(row=1,column=0,columnspan=len(self.imgs)*2,sticky="e")
        self.draw_tl()

    def draw_tl(self):
        for l in self.imgs:
            l["button"].configure(anchor = "nw", activebackground = "#33B5E5", relief = "flat",command = lambda i=l["index"]: self.setActive(i))
            self.tlbuttons.append(self.t.create_window(0,l["index"]*100,anchor="nw",window=l["button"]))
            l["button"].pack(side="left")
        if not self.n == []:
            self.n.append ( ImageTk.PhotoImage(self.n[0]) )
            self.activeimg = tk.Label(self.acf,image=self.n[2],relief="raised")
            self.c.create_image(0,0,image=self.n[2],anchor="nw")

    def say_hi(self):
        print("hi there, everyone!")

    def render(self):
        self.tl.render("./tl",fd.asksaveasfilename(defaultextension="*.mp4"))

    def save(self):
        self.tl.save(fd.asksaveasfilename(defaultextension="*.cowboytl"))

    def delete(self):
        print(self.n)
        self.tl.delete(self.n[1])
        self.update_tl()

    def loadFromFile(self):
        self.tl=tlbase.cowboytimeline(fromFile=True,file=fd.askopenfilename())
        self.update_tl()

    def insert(self):
        self.tl.insert(tksd.askinteger(title="Insert",prompt ="Insert at what frame?",parent=self),Image.open(fd.askopenfilename())) #TODO: seperate window with frame + file browser
        self.update_tl()

    def replace(self):
        self.tl.replace(tksd.askinteger(title="Insert",prompt ="Insert at what frame?",parent=self),Image.open(fd.askopenfilename())) #TODO: seperate window with frame + file browser
        self.update_tl()

    def setActive(self,ind):
        #print("called",ind)
        self.n = []
        self.n.append ( self.tl.get(ind))
        self.n.append(ind)
        self.n[0].resize(( math.ceil(10/self.n[0].width) , math.ceil(10/self.n[0].height) ),Image.ANTIALIAS)
        #self.n.show()
        self.draw_tl()
    

tl = tlbase.cowboytimeline(contents = [Image.open("pupyup.png"),Image.open("icecream.png")])
root = tk.Tk()
root.geometry("1000x800")
app = Application(tl,master=root)
app.mainloop()
