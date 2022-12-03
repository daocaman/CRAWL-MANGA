from skimage.metrics import structural_similarity as compare_ssim
import cv2
import os

checkFolder = "Check"

shapes = []

imgs = []

for img in os.listdir(checkFolder):
    tmpImg = cv2.imread(checkFolder+"/"+img)
    tmpImg = cv2.cvtColor(tmpImg, cv2.COLOR_BGR2GRAY)

    shapes.append(tmpImg.shape)

    imgs.append(tmpImg)

listFiles = os.listdir()

if checkFolder in listFiles:
    listFiles.remove(checkFolder)


for fol in listFiles:
    if os.path.isdir(fol):
        for img in os.listdir(fol):
            if os.path.isfile(fol+"/"+img):
                # print(fol+"/"+img)
                imgB = cv2.imread("./"+fol+"/"+img)
                # cv2.imshow("test",imgB)
                imgB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)
                if imgB.shape in shapes:
                    for i in imgs:
                        if imgB.shape == i.shape:
                            (score, diff) = compare_ssim(i, imgB, full=True)
                            if score > 0.9:
                                print(score)
                                os.remove(fol+"/"+img)
