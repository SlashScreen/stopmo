from PIL import Image
from zipfile import ZipFile
import ast

class cowboytimeline:
    def __init__(self,contents=[],data=[],fromFile=False,file=None):
        self.tl={}
        self.tl["frames"] = []
        self.tl["mdata"] = []
        if not fromFile:
            self.tl["frames"]=contents
            if data == []:
                self.tl["mdata"] = [self.tl["frames"][0].size,self.tl["frames"][0].format,0]
            else:
                self.tl["mdata"]=data
        else:
            with ZipFile(file) as archive:
                for i in range (len(archive.infolist())-1):
                    with archive.open("tl/{i}.png".format(i=i)) as file:
                        self.tl["frames"].append(Image.open(file))
            f = open("./tl/tl.cbtldat","r+")
            lines = f.read().splitlines()
            self.tl["mdata"].append(tuple(ast.literal_eval(lines[0])))
            self.tl["mdata"].append(lines[1])
            self.tl["mdata"].append(int(lines[2]))
            #More data stored in here: duration?

    def get(self,frame=None):
        if frame is None:
            return self.tl["frames"]
        else:
            return self.tl["frames"][frame-1]

    def getMData(self):
        return self.tl["mdata"]

    def compileMDataFile(self,dat):
        out = []
        out.append(list(dat[0]))
        out.append(str(dat[1]))
        out.append(str(dat[2]))
        return out

    def updateMData(self):
        self.tl["mdata"][2] = len(self.tl["frames"])

    def insert(self,frame,value):
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["frames"][0].size,color=0))
            self.tl["frames"].append(value)
        else:
            self.tl["frames"].insert(frame,value)
        self.updateMData()

    def replace(self,frame,value):
        if frame > len(self.tl["frames"]):
            for f in range(frame-len(self.tl)):
                self.tl["frames"].append(Image.new("RGB",self.tl["frames"][0].size,color=0))
            self.tl["frames"].append(value)
        else:
            self.tl["frames"][frame]=value
        self.updateMData()

    def save(self,filename):
        
        f= open("./tl/tl.cbtldat","w+")
        with ZipFile('{n}.cowboytl'.format(n=filename), 'w') as archive:
            i=0
            for v in self.get():
                v.save("./tl/{f}.png".format(f=i),"PNG")
                archive.write("./tl/{f}.png".format(f=i))
                if i == (len(test.get())-1):
                    i=i
                else:
                    i+=1
            for d in self.compileMDataFile(self.tl["mdata"]): 
                f.write(str(d)+"\n")
            archive.write("./tl/tl.cbtldat")
        f.close()


if __name__ == "__main__":
    test = cowboytimeline(contents = [Image.open("krime.png"),Image.open("evil.png")])
    test.insert(10,Image.open("intro2.png"))
    test.insert(3,Image.open("drfuchs.png"))
    test.replace(4,Image.open("intro1.png"))
    test.save("./savedtl")
    also = cowboytimeline(fromFile=True,file="savedtl.cowboytl")
    also.save("./othertl")

