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
        self.n = None
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
            tlimg = {}
            tlimg["index"] = i
            tlimg["button"] = tk.Button(self,image = self.tlimgs[i])#,command = lambda: self.setActive(self.tlimg["index"])) #tk.Label(self,image = self.tlimgs[i])
            self.imgs.append(tlimg)
            #self.tlimg["button"].grid(row=5,column=i)
            #self.entry = tk.Label(text=str(i))
            #self.entry.grid(row=6,column=i)
            i+=1
        
        self.draw_tl()

    def draw_tl(self):
        for l in self.imgs:
            print(l["index"],"index")
            print(self.active)
            l["button"].configure(command = lambda: self.setActive(l["index"]))
            l["button"].grid(row=5,column=l["index"])
        if not self.active == None:
            self.newactiveimage = self.active
            self.activeimg = tk.Label(self,image=self.newactiveimage)
            self.activeimg.grid(row=6,column=0)
            self.draw_tl()

    def say_hi(self):
        print("hi there, everyone!")

    def insert(self):
        tl.insert(6,Image.open("drfuchs.png")) #TODO: seperate window with frame + file browser
        self.update_tl()

    def setActive(self,ind):
        print("called",ind)
        self.n = self.tl.get(ind)
        self.n.resize((200,int(self.n.height*200/self.n.width)))
        self.active = ImageTk.PhotoImage(self.n)
        print(self.active)
        #self.n.show()
        #self.update_tl()
    

tl = tlbase.cowboytimeline(contents = [Image.open("pupyup.png"),Image.open("icecream.png")])
root = tk.Tk()
root.geometry("1000x800")
app = Application(tl,master=root)
app.mainloop()
