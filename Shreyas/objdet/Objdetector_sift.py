import cv2
import numpy as np

MIN_MATCH_COUNT = 35 #Vary according to background setup #depends on the adaptive brightness
detector = cv2.SIFT()
FLANN_INDEX_KDTREE = 0
flannParam = dict(algorithm = FLANN_INDEX_KDTREE, tree=5)
flann = cv2.FlannBasedMatcher(flannParam,{})

#load training image

trainImg = cv2.imread("rpi.jpg",0)
#"directory/imgName.jpg" #I stored my image in the pgm dir itself
trainKp,trainDesc = detector.detectAndCompute(trainImg,None)

cam = cv2.VideoCapture(0)
while True:
    ret,OriginalImgBGR = cam.read()
    if ret:
        OriginalImgGray = cv2.cvtColor(OriginalImgBGR, cv2.COLOR_BGR2GRAY)
        ImgKp,ImgDesc = detector.detectAndCompute(OriginalImgGray,None)
        matches = flann.knnMatch(ImgDesc,trainDesc,k=2)

        goodMatch = []
    
        for m,n in matches:
            if(m.distance<0.75*n.distance):
                goodMatch.append(m)

        if(len(goodMatch) > MIN_MATCH_COUNT):
            tKp=[]
            IKp=[]
            for m in goodMatch:
                tKp.append(trainKp[m.trainIdx].pt)
                #trainIdx is predefined need to be written as it is 
                IKp.append(ImgKp[m.queryIdx].pt)
                #queryIdx is predefined need to be written as it is

            tKp,IKp = np.float32((tKp,IKp))
            H,status = cv2.findHomography(tKp,IKp,cv2.RANSAC,3.0)
            #3.0 here varies with the brigtness and clarity
            # no clear explaination given on OpenCV website
            h,w = trainImg.shape
            trainingBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
            ImgBorder = cv2.perspectiveTransform(trainingBorder, H)
            cv2.polylines(OriginalImgBGR, [np.int32(ImgBorder)],True,(0,255,0),4)

        else:
            print("Not Enough matches - " + str(len(goodMatch))+ "/" + str(MIN_MATCH_COUNT))

        cv2.imshow('result img', OriginalImgBGR)
        if cv2.waitKey(10)==ord('q'):
            break
cam.release()
cv2.destroyAllWindows()

    
    
