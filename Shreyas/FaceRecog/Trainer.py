import cv2
import os
import numpy as np
from PIL import Image


recognizer = cv2.createLBPHFaceRecognizer()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
path = 'DataSet'

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage,'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        IDs.append(Id)
        cv2.imshow("Training",imageNp)
        cv2.waitKey(10)
        return faces, np.array(IDs)

faces,Ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(Ids))
recognizer.save('trainer.yml')
cv2.destroyAllWindows()
