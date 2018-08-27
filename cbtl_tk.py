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
        self.active = None
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
            self.tlimg = {}
            self.tlimg["index"] = i
            self.tlimg["button"] = tk.Button(self,image = self.tlimgs[i],command = lambda: self.setActive(self.tlimg["index"])) #tk.Label(self,image = self.tlimgs[i])
            self.tlimg["button"].grid(row=5,column=i)
            #self.entry = tk.Label(text=str(i))
            #self.entry.grid(row=6,column=i)
            i+=1
        self.activeimg = tk.Label(image=self.active)
        self.activeimg.grid(row=6,column=1)

    def say_hi(self):
        print("hi there, everyone!")

    def insert(self):
        tl.insert(6,Image.open("drfuchs.png")) #TODO: seperate window with frame + file browser
        self.update_tl()

    def setActive(self,ind):
        print("called",ind)
        n = self.tl.get(ind)
        n.resize((600,int(n.height*600/n.width)))
        self.active = ImageTk.PhotoImage(n)
        self.update_tl()
    

tl = tlbase.cowboytimeline(contents = [Image.open("pupyup.png"),Image.open("icecream.png")])
root = tk.Tk()
root.geometry("1000x800")
app = Application(tl,master=root)
app.mainloop()
