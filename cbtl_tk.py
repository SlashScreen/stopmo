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
        print("Hi made")

        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="top")
        print("Quit made")

        #tlcanvas = tk.Canvas(root, width = 300, height = 300)
        #tlcanvas.pack()
        #tlcanvas.create_line(0, 20, 300, 20, fill="#476042")
        
        i=0
 #       root.img = []
        self.lbl = tk.Label(self, text="actually work thank")
        self.lbl.pack()
        self.thumbs = self.tl.genThumb()
        self.test = tk.Label(self,image = ImageTk.PhotoImage(self.thumbs[0]))
        self.test.pack()
 #       print(self.test)
        
        #for v in self.tl.get():
 #          n=ImageTk.PhotoImage(v)
 #         self.imgs.append(tk.Label(root,image=n))
 #          self.imgs[i].pack()
 #          i+=1


           
            #v.show()
 #           root.img.append(n)
 #           tlcanvas.create_image(20*i,20,image=n)
        #print("Canvas made")
        #print(tlcanvas)
        

    def say_hi(self):
        print("hi there, everyone!")

tl = tlbase.cowboytimeline()
root = tk.Tk()
app = Application(tl,master=root)
app.mainloop()
