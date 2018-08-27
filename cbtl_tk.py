import tkinter as tk
import cbtl_base as tlbase
import cbtl_tween as tween
import cbtl_video as video
from PIL import Image,ImageTk


        

class Application(tk.Frame):
    def __init__(self,tl, master=None):
        super().__init__(master)
        self.tl = tl
        #self.pack()
        self.grid()
        self.imgs = []
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
        for t in self.thumbs:
            self.tlimgs.append(ImageTk.PhotoImage(t))
            self.tlimg = tk.Label(self,image = self.tlimgs[i])
            self.tlimg.grid(row=5,column=i)
            #self.entry = tk.Label(text=str(i))
            #self.entry.grid(row=6,column=i)
            i+=1

    def say_hi(self):
        print("hi there, everyone!")

    def insert(self):
        tl.insert(6,Image.open("drfuchs.png"))
        self.update_tl()

tl = tlbase.cowboytimeline(contents = [Image.open("krime.png"),Image.open("evil.png")])
root = tk.Tk()
root.geometry("1000x800")
app = Application(tl,master=root)
app.mainloop()
