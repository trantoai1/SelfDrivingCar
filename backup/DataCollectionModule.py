"""
- This module saves images and a log file.
- Images are saved in a folder.
- Folder should be created manually with the name "DataCollected"
- The name of the image and the steering angle is logged
in the log file.
- Call the saveData function to start.
- Call the saveLog function to end.
- If runs independent, will save ten images as a demo.
"""

import pandas as pd
import os
import cv2
from datetime import datetime
class DataCollectionModule:
    def __init__(self,folder='DataCollected',countFolder=0):
        self.countFolder = countFolder
        self.count = 0
        self.imgList = []
        self.steeringList = []
        self.speedList = []
        self.folder = folder
        # GET CURRENT DIRECTORY PATH
        self.myDirectory = os.path.join('/media/pi/4A14-BA7C', folder)
        self.newPath = ''
        self.countCurrentFolder()
    def countCurrentFolder(self):
        while os.path.exists(os.path.join(self.myDirectory, f'IMG{str(self.countFolder)}')):
            self.countFolder += 1
        self.newPath = self.myDirectory + "/IMG" + str(self.countFolder)
        os.makedirs(self.newPath)

    def saveData(self,img, steering, speed):

        now = datetime.now()
        timestamp = str(datetime.timestamp(now)).replace('.', '')
        # print("timestamp =", timestamp)
        fileName2 = 'Image_{}.jpg'.format(timestamp)
        fileName = os.path.join(self.newPath, fileName2)
        fileName_csv = os.path.join(
            '/content/gdrive/My Drive/SSL/Embedded/Step2-Training/'+self.folder + "/IMG" + str(self.countFolder), fileName2)
        cv2.imwrite(fileName, img)
        self.imgList.append(fileName_csv)
        self.steeringList.append(steering)
        self.speedList.append(speed)

    # SAVE LOG FILE WHEN THE SESSION ENDS
    def saveLog(self):

        rawData = {'Image': self.imgList,
                   'Steering': self.steeringList, 'Speed': self.speedList}
        df = pd.DataFrame(rawData)
        df.to_csv(os.path.join(self.myDirectory, f'log_{str(self.countFolder)}.csv'), index=False, header=False)
        print('Log Saved')
        print('Total Images: ', len(self.imgList))
#print(myDirectory)

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT


# SAVE IMAGES IN THE FOLDER

