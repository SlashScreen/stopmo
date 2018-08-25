from PIL import Image
import cbtl_base

def generateInbetweens(tl,a = .5):
    inserts = {}
    for f in range(len(tl.get())):
        print(f)
        if not f==0:
            inserts[f] = Image.blend(tl.get(f),tl.get(f-1),a)
            #tl.insert(f,tween)
    pos = list(inserts.keys())
    vals = list(inserts.values())
    for f in range(len(inserts)):
        #print(f,pos[f],vals[f])
        tl.insert(pos[f],vals[f])
        
    
    tl.changeFPS(tl.getMData()["fps"]*2)
    #print("tween",tl.getMData())


if __name__ == "__main__":
    test = cbtl_base.cowboytimeline(contents = [Image.open("intro1.png"),Image.open("intro2.png")])
    generateInbetweens(test)
    test.save("./between",debug = True)
    test.render("./tl","./between.mp4")
