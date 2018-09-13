import tkinter as tk
from tkinter import filedialog as fd
import tkinter.simpledialog as tksd
import cbtl_base as tlbase
import cbtl_tween as tween
import cbtl_video as video
from PIL import Image,ImageTk
import math
import ast

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
        try:
            f=open("./appfiles/cache.data","r+")
            lines = f.read()
            tempcache = ast.literal_eval(lines)
            self.currentfilepath=tempcache["lastfile"]
            #print(self.currentfilepath)
            self.loadFromFile(fromCache=True)
        except Exception as e:
            print(e)
            self.currentfilepath = ""
        self.create_widgets()
        self.setActive(0)
        self.tlbuttons = []

        

    def create_widgets(self):
        self.toolbarf = tk.Frame(self,bg="black",width=100,height=100)
        self.toolbarc = tk.Canvas(self.toolbarf,width=50, height=50)
        self.toolbarf.grid(row=0,column=0,sticky="e")
        self.toolbarc.pack(side="left")
        
        self.toolbarm = tk.Menu(self)
        self.toolbarm_file = tk.Menu(self.toolbarm)
        self.toolbarm_video = tk.Menu(self.toolbarm)
        self.toolbarm.add_cascade(label="File", menu=self.toolbarm_file)
        self.toolbarm.add_cascade(label="Video", menu=self.toolbarm_video)

        self.toolbarm_file.add_command(label="New", command=self.new)
        self.toolbarm_file.add_command(label="Save", command=self.save)
        self.toolbarm_file.add_command(label="Load", command=self.loadFromFile)
        self.toolbarm_file.add_separator()
        self.toolbarm_file.add_command(label="Delete", command=self.delete)
        self.toolbarm_file.add_command(label="Insert", command=self.insert)
        self.toolbarm_file.add_command(label="Replace", command=self.replace)
        self.toolbarm_file.add_command(label="Append", command=self.append)
        self.toolbarm_file.add_command(label="Generate Inbetweens", command=self.tween)
        self.toolbarm_file.add_separator()
        self.toolbarm_file.add_command(label="Quit", command=self.quit)

        self.toolbarm_video.add_command(label="Render", command=self.render)
        self.toolbarm_video.add_command(label="Change FPS", command=self.changeFPS)
        #self.toolbarf.config(menu=self.toolbarm)
        
        self.update_tl()
 #       tk.after(30, self.update_tl())

    def update_tl(self):
        i=0
        for child in self.imgs:
            #if isinstance(child, tk.Button):
            #print("destroyed")
            child["button"].destroy()
        self.filepath_l = tk.Label(text="Current filepath: "+self.currentfilepath)
        self.filepath_l.grid(row=1,column=0)
        self.thumbs = self.tl.genThumb()
        self.tlimgs = []
        self.imgs = []
        self.acf = tk.Frame(self,bg="black",width=100,height=100)
        self.acf.grid(row=6,column=0)
        self.tlf = tk.Frame(self,bg="red",width=100,height=100)
        
        
        self.c = tk.Canvas(self.acf,width=600, height=300)
        self.c.pack()
        
        self.t = tk.Canvas(self.tlf,width=800, height=300,)
        self.t.pack(side="left",expand = False)
        self.hscrollbar = tk.Scrollbar(self.t, orient = "horizontal")
        self.hscrollbar.pack(fill = "x", side = "bottom", expand = False)
        
        self.t.configure(xscrollcommand = self.hscrollbar.set)
        self.t.xview_moveto(0)
        self.hscrollbar.config(command = self.t.xview)
        
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
        #print(len(self.imgs),self.tl.getMData()["duration"])
        for l in self.imgs:
            l["button"].configure(anchor = "nw", activebackground = "#33B5E5", relief = "flat",command = lambda i=l["index"]: self.setActive(i))
            self.tlbuttons.append(self.t.create_window(0,l["index"]*100,anchor="nw",window=l["button"],tags=("tlbutton")))
            l["button"].pack(side="left")
        if not self.n == []:
            self.n.append ( ImageTk.PhotoImage(self.n[0]) )
            print(len(self.n))
            self.activeimg = tk.Label(self.acf,image=self.n[2],relief="raised")
            self.c.create_image(0,0,image=self.n[2],anchor="nw")
        

    def say_hi(self):
        print("hi there, everyone!")

    def tween(self):
        tween.generateInbetweens(self.tl,a=.5)
        self.update_tl()

    def new(self):
        self.tl=tlbase.cowboytimeline()
        self.currentfilepath = ""
        self.update_tl()

    def render(self):
        self.tl.render("./tl",fd.asksaveasfilename(defaultextension="*.mp4"))

    def save(self):
        path = fd.asksaveasfilename(defaultextension="*.cowboytl")
        self.tl.save(path)
        self.currentfilepath = path

    def quit(self):
        self.save()
        cache = {}
        cache["lastfile"] = self.currentfilepath
        f= open("./appfiles/cache.data","w+")
        f.write(str(cache))
        f.close()
        root.destroy()

    def delete(self):
        self.tl.delete(self.n[1])
        del self.thumbs[self.n[1]]
        del self.tlbuttons[self.n[1]]
        self.update_tl()

    def loadFromFile(self,fromCache=False):
        if not fromCache:           
            self.currentfilepath = fd.askopenfilename()
        self.tl=tlbase.cowboytimeline(fromFile=True,file=self.currentfilepath)
        if not fromCache:
            self.update_tl()

    def changeFPS(self):
        #print("changeFPS")
        self.tl.changeFPS(tksd.askfloat(title="FPS",prompt ="What to change FPS to?",parent=self))

    def insert(self):
        self.tl.insert(tksd.askinteger(title="Insert",prompt ="Insert at what frame?",parent=self),Image.open(fd.askopenfilename())) #TODO: seperate window with frame + file browser
        self.update_tl()

    def append(self):
        self.tl.append(Image.open(fd.askopenfilename())) #TODO: seperate window with frame + file browser
        self.update_tl()

    def replace(self):
        self.tl.replace(tksd.askinteger(title="Insert",prompt ="Insert at what frame?",parent=self),Image.open(fd.askopenfilename())) #TODO: seperate window with frame + file browser
        self.update_tl()

    def setActive(self,ind):
        #print("called",ind)
        self.n = []
        self.n.append ( self.tl.get(ind))
        self.n.append(ind)
        self.n[0].resize(( math.ceil(200/self.n[0].width) , math.ceil(200/self.n[0].height) ),Image.ANTIALIAS)
        #self.n.show()
        self.draw_tl()
    

tl = tlbase.cowboytimeline()#contents = [Image.open("pupyup.png"),Image.open("icecream.png")])
root = tk.Tk()
root.geometry("1000x800")

app = Application(tl,master=root)
root.config(menu=app.toolbarm)
app.mainloop()
