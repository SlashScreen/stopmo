from PIL import Image
import cbtl_base

def generateInbetweens(tl,a = .5):
    for f in range(len(tl.get())):
        tween = Image.blend(tl.get(f-1),tl.get(f),a)
        tl.insert(f,tween)
    tl.changeFPS(tl.getMData()["fps"]*2)

test = cbtl_base.cowboytimeline(contents = [Image.open("intro1.png"),Image.open("intro2.png")])
generateInbetweens(test)
test.render("./tl","./out/tween.mp4")
