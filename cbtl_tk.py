import tkinter as tk
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
        

    def create_widgets(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.grid(row=0,column=0)

        self.inserttest = tk.Button(self, text="INSERT", fg="red",command=self.insert)
        self.inserttest.grid(row=0,column=1)
        self.update_tl()
 #       tk.after(30, self.update_tl())

    def update_tl(self):
        i=0
        self.thumbs = self.tl.genThumb()
        self.tlimgs = []
        self.imgs = []
        for t in self.thumbs:
            self.tlimgs.append(ImageTk.PhotoImage(t))
            tlimg = {}
            tlimg["index"] = i
            tlimg["button"] = tk.Button(self,image = self.tlimgs[i],text = str(i),borderwidth=0)#,command = lambda: self.setActive(self.tlimg["index"])) #tk.Label(self,image = self.tlimgs[i])
            self.imgs.append(tlimg)
            #self.tlimg["button"].grid(row=5,column=i)
            #self.entry = tk.Label(text=str(i))
            #self.entry.grid(row=6,column=i)
            i+=1
        
        self.draw_tl()

    def draw_tl(self):
        for l in self.imgs:
            #print(int(l["button"]['text']),"text")
            #print(self.active)
            l["button"].configure(command = lambda i=l["index"]: self.setActive(i))
            l["button"].grid(row=5,column=l["index"])
        if not self.n == []:
            #print("yeah")
            self.n.append ( ImageTk.PhotoImage(self.n[0]) )
            self.activeimg = tk.Label(self,image=self.n[1],relief="raised")
            self.activeimg.grid(row=6,column=0,columnspan = 6)
            #print(self.activeimg)
            #self.draw_tl()

    def say_hi(self):
        print("hi there, everyone!")

    def insert(self):
        tl.insert(6,Image.open("drfuchs.png")) #TODO: seperate window with frame + file browser
        self.update_tl()

    def setActive(self,ind):
        #print("called",ind)
        self.n = []
        self.n.append ( self.tl.get(ind))
        self.n[0].resize(( math.ceil(600/self.n[0].width) , math.ceil(600/self.n[0].height) ))
        #self.n.show()
        self.draw_tl()
    

tl = tlbase.cowboytimeline(contents = [Image.open("pupyup.png"),Image.open("icecream.png")])
root = tk.Tk()
root.geometry("1000x800")
app = Application(tl,master=root)
app.mainloop()
