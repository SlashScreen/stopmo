import cbtl_base
from PIL import Image

def withinRange(px1,px2,tol):
    for i in range(2):
        if px1[i]-tol <= px2[i] <= px1[i]+tol:
            return False
    return True

def imgbool(img1,img2,tolerance):
    print(img1.size)
    pmer = img1.load()
    cntre = img2.load()
    origmask = Image.new("RGBA",img1.size,color = (0,0,0,255))
    mask = origmask.load()
    #thru all pixels: if they are not within tolerance range, write to mask.
    for y in range(img1.height):
        for x in range(img1.width):
            if not withinRange(pmer[x,y],cntre[x,y],tolerance):
                mask[x,y] = (0,0,0,0)
    #origmask.show()
    bg = Image.new("RGBA",img1.size,color = (0,255,0,255))
    return Image.composite(bg,img2,mask = origmask)

if __name__ == "__main__":
    intro1=Image.open("./intro1.png")
    intro2=Image.open("./intro2.png")
    imgbool(intro1,intro2,0).show()
    imgbool(intro1,intro2,2).show()
    imgbool(intro1,intro2,5).show()
    imgbool(intro1,intro2,15).show()
