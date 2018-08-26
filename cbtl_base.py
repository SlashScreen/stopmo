from PIL import Image,ImageFont,ImageDraw
from zipfile import ZipFile
import ast
import cv2
import os

def cleanFilename(string):
    return int(string.replace(".png",''))

class cowboytimeline:
    def __init__(self,contents=[],data={},fromFile=False,file=None):
        self.tl={}
        self.tl["frames"] = []
        self.tl["mdata"] = {}
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
            with ZipFile(file) as archive:
                for i in range (len(archive.infolist())-1):
                    with archive.open("tl/{i}.png".format(i=i)) as file:
                        self.tl["frames"].append(Image.open(file).resize(self.get(0).size))
            f = open("./tl/tl.cbtldat","r+")
            lines = f.read()
            self.tl["mdata"] = ast.literal_eval(lines)

    def get(self,frame=None):
        #print(frame)
        if frame is None:
            return self.tl["frames"]
        else:
            return self.tl["frames"][frame-1]

    def getMData(self):
        return self.tl["mdata"]

    def updateMData(self):
        #print (len(self.tl["frames"]))
        self.tl["mdata"]["duration"] = len(self.tl["frames"])

    def changeFPS(self,fps):
        self.tl["mdata"] = fps
        #self.updateMData()

    def insert(self,frame,value):
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["frames"][0].size,color=0))
            self.tl["frames"].append(value).resize(self.get(0).size)
        else:
            self.tl["frames"].insert(frame,value.resize(self.get(0).size))
        self.updateMData()

    def replace(self,frame,value):
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["frames"][0].size,color=0))
            self.tl["frames"].append(value.resize(self.get(0).size))
        else:
            self.tl["frames"][frame]=value.resize(self.get(0).size)
        self.updateMData()

    def delete(self,frame):
        self.tl["frames"].remove(frame-1)

    def append(self,img):
        self.tl["frames"].append(img.resize(self.get(0).size))

    def save(self,filename,debug=False):
        f= open("./tl/tl.cbtldat","w+")
        with ZipFile('{n}.cowboytl'.format(n=filename), 'w') as archive:
            i=0
            for v in self.get():
                if debug:
                    fnt = ImageFont.truetype('FreeMono.ttf', 40)
                    tmp = Image.new("RGB",self.tl["frames"][0].size,color=0).convert("RGBA")
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
            f.write(str(self.tl["mdata"]))
            archive.write("./tl/tl.cbtldat")
        f.close()

    def render(self,path,name):
        self.save('./temp') #make this changable
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
    test.save("./savedtl")
    also = cowboytimeline(fromFile=True,file="savedtl.cowboytl")
    test.insert(7,Image.open("drfuchs.png"))
    also.save("./othertl")
    also.render("./tl","./out/pleasework.mp4")

