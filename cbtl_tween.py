from PIL import Image
import cbtl_base

def generateInbetweens(tl,a = .5):
    inserts = {}
    size = tl.getMData()["size"]
    for f in range(len(tl.get())):
        if not f==0:
            inserts[f] = Image.blend(tl.get(f).convert('RGBA'),tl.get(f-1).convert('RGBA'),a)
    pos = list(inserts.keys())
    vals = list(inserts.values())
    for f in range(len(inserts)):
        tl.insert(pos[f]+2,vals[f])
    tl.changeFPS(tl.getMData()["fps"]*2)


if __name__ == "__main__":
    test = cbtl_base.cowboytimeline(contents = [Image.open("intro1.png"),Image.open("intro2.png")])
    generateInbetweens(test)
    test.save("./between",debug = True)
    test.render("./tl","./between.mp4")
