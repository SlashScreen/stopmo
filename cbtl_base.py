from PIL import Image,ImageFont,ImageDraw,ImageTk
from zipfile import ZipFile
import ast
import cv2
import os
from tkinter import Tk
from tkinter import filedialog
import shutil

def cleanFilename(string):
    return int(string.replace(".png",''))

def constructMData(size,form,dur,fps):
    mdata = {}
    mdata["size"] = size
    mdata["format"] = form
    mdata["duration"] = dur
    mdata["fps"] = fps
    return mdata



class cowboytimeline:
    def __init__(self,contents=[],data={},fromFile=False,file=None):
        self.tl={}
        self.tl["frames"] = []
        self.tl["mdata"] = {}
        #print(file)
        if not fromFile:
            if not contents == []:
                self.tl["frames"]=contents
            else:
                self.tl["frames"] = [Image.new("RGB",(1920,1080),color=0)]
            if data == {}:
                self.tl["mdata"] = {}
                self.tl["mdata"]["size"] = self.tl["frames"][0].size
                self.tl["mdata"]["format"] = self.tl["frames"][0].format
                if not len(self.tl["frames"]) is None:
                    self.tl["mdata"]["duration"] = len(self.tl["frames"])
                else:
                    self.tl["mdata"]["duration"] = 0
                self.tl["mdata"]["fps"] = 6
            else:
                self.tl["mdata"]=data
        else:
            #print("fromfile")
            with ZipFile(file) as archive:
                #f = open("./tl/tl.cbtldat","r+")
                lines = archive.read("tl/tl.cbtldat").decode("utf-8") 
                self.tl["mdata"] = ast.literal_eval(lines)
                for i in range (len(archive.infolist())-1):
                    with archive.open("tl/{i}.png".format(i=i)) as file:
                        if self.tl["frames"] == []:
                            self.tl["frames"].append(Image.open(file))
                        else:
                            #print(self.tl["mdata"])
                            self.tl["frames"].append(Image.open(file).resize(self.tl["mdata"]["size"]))
            

    def get(self,frame=None):
        if frame is None:
            return self.tl["frames"]
        else:
            return self.tl["frames"][frame]

    def genThumb(self):
        thumbs = []
        for v in self.tl["frames"]:
            n = v.copy()
            n.thumbnail((200,int(self.getMData()["size"][1]*(200/(self.getMData()["size"][0]) ) )) )
            thumbs.append(n)
        return thumbs
    
    def getMData(self):
        return self.tl["mdata"]

    def updateMData(self):
        #print (len(self.tl["frames"]))
        self.tl["mdata"]["duration"] = len(self.tl["frames"])

    def changeFPS(self,fps):
        self.tl["mdata"]["fps"] = fps
        #self.updateMData()

    def insert(self,frame,value):
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["mdata"]["size"],color=0))
            self.tl["frames"].append(value.resize(self.get(0).size))
        else:
            self.tl["frames"].insert(frame-1,value.resize(self.tl["mdata"]["size"]))
        self.updateMData()

    def replace(self,frame,value):
        #print(value)
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["mdata"]["size"],color=0))
            self.tl["frames"].append(value.resize(self.tl["mdata"]["size"]))
        else:
            self.tl["frames"][frame-1]=value.resize(self.tl["mdata"]["size"])
        self.updateMData()

    def delete(self,frame):
        del self.tl["frames"][frame]
        self.updateMData()

    def append(self,img):
        self.tl["frames"].append(img.resize(self.tl["mdata"]["size"]))

    def save(self,filename,debug=False):
        shutil.rmtree('./tl/')
        os.makedirs("./tl")
        with ZipFile(filename, 'w') as archive:
            i=0
            for v in self.get():
                if debug:
                    fnt = ImageFont.truetype('FreeMono.ttf', 40)
                    tmp = Image.new("RGB",self.tl["mdata"]["size"],color=0).convert("RGBA")
                    d = ImageDraw.Draw(tmp)
                    d.text((0,0), str(i), font=fnt, fill=(255,255,255,128))
                    out = Image.alpha_composite(v.convert("RGBA"), tmp)
                    #out.show()
                    out.save("./tl/{f}.png".format(f=i),"PNG")
                else:
                    v.save("./tl/{f}.png".format(f=i),"PNG")
                archive.write("./tl/{f}.png".format(f=i))
                if i == (len(self.tl["frames"])-1):
                    i=i
                else:
                    i+=1
            tldat = str(self.tl["mdata"])
            f= open("./tl/tl.cbtldat","w+")
            #print (tldat)
            f.write(tldat)
            #print("file:",f.read())
            archive.write("./tl/tl.cbtldat")
        f.close()

    def render(self,path,name):
        self.save(filedialog.asksaveasfilename(defaultextension="*.cowboytl"))
        image_folder = path
        video_name = name

        images = sorted([img for img in sorted(os.listdir(image_folder)) if img.endswith(".png")],key=cleanFilename)
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, -1, self.getMData()["fps"], (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()


if __name__ == "__main__":
    test = cowboytimeline(contents = [Image.open("krime.png"),Image.open("evil.png")])
    test.insert(10,Image.open("intro2.png"))
    test.insert(3,Image.open("drfuchs.png"))
    test.replace(4,Image.open("intro1.png"))
    test.save(filedialog.asksaveasfilename(defaultextension="*.cowboytl"))
    also = cowboytimeline(fromFile=True,file=filedialog.askopenfilename())
    test.insert(7,Image.open("drfuchs.png"))
    also.save(filedialog.asksaveasfilename(defaultextension="*.cowboytl"))
    also.render("./tl",filedialog.asksaveasfilename(defaultextension="*.mp4"))

