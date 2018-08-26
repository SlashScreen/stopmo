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
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="top")

        self.inserttest = tk.Button(self, text="INSERT", fg="red",command=self.say_hi())
        self.inserttest.pack(side="right")
        
        i=0
        self.thumbs = self.tl.genThumb()
        self.tlimgs = []
        for t in self.thumbs:
            self.tlimgs.append(ImageTk.PhotoImage(t))
            self.tlimg = tk.Label(self,image = self.tlimgs[i])
            self.tlimg.pack(side="left")
            i+=1

    def say_hi(self):
        print("hi there, everyone!")

    def insert(self):
        self.tl.insert(6,Image.open("drfuchs.png"))

tl = tlbase.cowboytimeline(contents = [Image.open("krime.png"),Image.open("evil.png")])
root = tk.Tk()
app = Application(tl,master=root)
app.mainloop()
