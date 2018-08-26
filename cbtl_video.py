import cv2, time
from PIL import Image
import cbtl_base

def capture(img,tl):
    cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    out = Image.fromarray(cv2_im)
    tl.append(out)
    out.show()


def captureWindow(tl):
    cam = cv2.VideoCapture(0)
    playing = True
    a=0
    while playing:
        a=a+1
        check,frame = cam.read()
        cv2.imshow("Capturing",frame)
        key=cv2.waitKey(1)
        if key == ord('q'):
            playing = False
        if key == ord('c'):
            capture(frame,tl)
    cam.release()

if __name__ == "__main__":
    tl = cbtl_base.cowboytimeline()
    captureWindow(tl)
    tl.save("./capturetl")
    print(tl.get())
    tl.render("./tl","./capture.mp4")
