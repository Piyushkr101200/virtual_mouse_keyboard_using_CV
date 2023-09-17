import HandTrackingModule as htm
import cv2 as cv
import numpy as np
import pyautogui 
import speech_recognition as sr
from pynput.keyboard import Key, Controller 
import time

wCam , hCam = 640,480
wScr , hScr =pyautogui.size()
frameR = 150
smootheing = 5
plocX , plocY = 0,0
clocX , clocY = 0,0

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.HandDetector()

def Mouse(img):
    global frameR
    global smootheing
    global plocX
    global plocY
    global clocX
    global clocY
    global wScr
    global wCam
    global hScr
    global hCam
    
    # 1.finding hands
    detector.findhands(img)
    lmlist, bbox = detector.findPosition(img)

    cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    if len(lmlist) != 0:
        
        # 2. check which finger is up?
        fingers = detector.fingersUp()
        # print(fingers)
        
        # 3. get the tip of index and midel finger 
        Xindex, Yindex = lmlist[8][1], lmlist[8][2]
        Xmidel, Ymidel = lmlist[12][1], lmlist[12][2]
        # 4. index: moving mode- move curser
        if fingers[1] == 1 and fingers[2] == 0:
            # i. cordinates the position (cam :640*480) to (screen :2560 × 1600)
            xMOUSE = np.interp(Xindex, (frameR, wCam - frameR), (0, wScr))
            yMOUSE = np.interp(Yindex, (frameR, hCam - frameR), (0, hScr))
            # ii. smoothen value
            clocX = plocX + (xMOUSE - plocX) / smootheing
            clocY = plocY + (yMOUSE - plocY) / smootheing
            # iii. move mouse 
            pyautogui.moveTo(clocX, clocY)
            # cv.circle(img, (Xindex, Yindex), 15, (20, 180, 90), cv.FILLED)
            plocY, plocX = clocY, clocX

        # 5. Index and Middle are up-right click 
        if fingers[1]  and fingers[2]  and fingers[3] == 0 and fingers[4] == 0:
            # i. finding distance
            length, bbox = detector.findDistance(8, 12, img)
            #print(length)
            # ii. click if distance was short
            if length < 30:
                pyautogui.rightClick()
                
        # 6. Index and Thumb are up left-right click 
        if fingers[1] and fingers[0] and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # i. Finding distance
            length, bbox = detector.findDistance(8, 4, img)
            #print(length)
            # ii. Click if distance was short
            if length < 40:
                pyautogui.leftClick()
                
        # 7. Index, Middle and Ring for down Scroll 
        if fingers[1] and fingers[2] and fingers[3] and fingers[4] == 0:
            pyautogui.scroll(-50)
        # 8. Pinkie, Ring and Middle for Up Scroll    
        if fingers[2]  and fingers[3] and fingers[4] and fingers[1] == 0:
            pyautogui.scroll(50)

        # 9. Audio to text converter 
        if fingers[1]==1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            r=sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Please say Something..")

                audio = r.listen(source)

                try:
                    keyboard = Controller()
                    time.sleep(2)
                    for char in r.recognize_google(audio) + " ":
                        keyboard.press(char)
                        keyboard.release(char)
                        time.sleep(0.12)

                except Exception as e:
                    print("Error :" + str(e))
            
    return img


def main():
    while True:
        sucess, img = cap.read()
        img = cv.flip(img, 1)

        img = Mouse(img)

        # 11. display

        cv.imshow("result", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    main()
