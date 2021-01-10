import time
import redis
import os
import time
import cv2
import json

configFileLocation = os.getenv('alarm_config_location') 
if not configFileLocation :
    configFileLocation = '../appsettings.json'
    
configFile = open(configFileLocation)
config = json.load(configFile)

def capture_image(cameraID, cameraURL, imageFolder):
    # function captures image from RTSP stream
    cap = cv2.VideoCapture(cameraURL)
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            img_name = str(cameraID) + '_' + str(time.time()).replace('.','_') + '.jpg'
            cv2.imwrite(imageFolder + img_name,image)
            return img_name
#TODO: read from config        
r = redis.Redis(host=config['Redis']['ip'], port=config['Redis']['port'], db=0, password=config['Redis']['password'])
r_pubsub = r.pubsub()

def my_callback(self):
    camera_id = int(self['data'])
    #IF we have a camera configured for this zone then capture image
    try :
        camera_url = config['Camera']['Zones'][camera_id]
        img_folder = config['Camera']['ImageFolder']
        if camera_url:
            print ('Capture image from Camera nr. ' + str(camera_id))
            img_name = capture_image(camera_id,camera_url,img_folder)
            r.publish('IMAGE_CAPTURED',img_name)
        else:
            print('Camera not configured for zone:' + str(camera_id))
    except IndexError:
        print('Camera configuration not found for zone: '+ str(camera_id))

r_pubsub.subscribe(**{'ALARM_TRIGGER':my_callback})
r_pubsub.run_in_thread(sleep_time=0.001)

while True:
    time.sleep(1)
