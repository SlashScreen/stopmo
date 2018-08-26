import tkinter as tk
import cbtl_base as tlbase
import cbtl_tween as tween
import cbtl_video as video
from PIL import Image,ImageTk

class Application(tk.Frame):
    def __init__(self,tl, master=None):
        super().__init__(master)
        self.tl = tl
        self.pack()
        self.grid()
        self.imgs = []
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="top")
        
        i=0
        self.lbl = tk.Label(self, text="actually work thank")
        self.lbl.pack()
        self.thumbs = self.tl.genThumb()
        self.test = tk.Label(self,image = ImageTk.PhotoImage(self.thumbs[0]))
        self.test.pack()
        self.tlimgs = []
        for t in self.thumbs:
            self.tlimgs.append(ImageTk.PhotoImage(t))
            self.tlimg = tk.Label(self,image = self.tlimgs[i])
            self.tlimg.pack(side="bottom")
            i+=1

    def say_hi(self):
        print("hi there, everyone!")

tl = tlbase.cowboytimeline(contents = [Image.open("krime.png"),Image.open("evil.png")])
root = tk.Tk()
app = Application(tl,master=root)
app.mainloop()
