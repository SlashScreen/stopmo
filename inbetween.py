from PIL import Image

imgs = [Image.open("intro1.png"),Image.open("intro2.png")]
tween = Image.blend(imgs[0],imgs[1],.7)
tween.show()
