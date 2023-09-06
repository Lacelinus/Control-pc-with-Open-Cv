import cv2
from mediapipe import solutions
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui as pg
import time 

#%%

# Capture video stream from the camera (0 for the local camera)
cap = cv2.VideoCapture(0)

# Import drawing functions from the mediapipe library
mpDraw = solutions.drawing_utils

# Import the hand detection (hands) model from the mediapipe library
mpHands = solutions.hands

# Initialize the Hands class to detect at most one hand
hands = mpHands.Hands(max_num_hands=1)

# Get audio devices (e.g., speakers)
devices = AudioUtilities.GetSpeakers()

# Activate an interface to change the system volume
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Use the IAudioEndpointVolume interface to control the audio
volume = interface.QueryInterface(IAudioEndpointVolume)

#%%

# Define color coding (Blue color)
color = (0, 255, 255)

# List containing the indexes of relevant hand landmarks
idlist = (13, 15)

# An empty list to store measured distances
dislist = []

# An empty list to store audio volume ratios
ratio = []

# Initial audio volume (in percentage, starting at 50%)
vol = 50

  
#%%

# Define a function to set the system volume
def set_system_volume(new_volume):
    
    # Get audio devices (e.g., speakers)
    devices = AudioUtilities.GetSpeakers()
    
    # Activate an interface to change the audio volume
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
    # Control audio using the IAudioEndpointVolume interface
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set the new volume level on a specified scale (0.0 - 1.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

#%%

def draw_volume_on_image(img, volume):
    cv2.putText(img, f"Volume Level: {volume}%", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


#%%

# Start an infinite loop that runs continuously
while True:
    # Read a video frame from the camera and assign it to 'sucsess' and 'img2' variables.
    sucsess, img2 = cap.read()
    
    # Convert the read frame from BGR color format to RGB color format and store it in the 'imgRGB' variable.
    # The reason for converting to RGB format is that the model for hand detection supports RGB format.
    imgRGB = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    # Process the image with mediapipe to detect hands and store the results in the 'results' variable.
    results = hands.process(imgRGB)
        
    # If more than one hand is detected:
    if results.multi_hand_landmarks:
        # Start a loop for each hand.
        for handlms in results.multi_hand_landmarks:
            # Draw landmarks of the hands and overlay them on the frame.
            mpDraw.draw_landmarks(img2, handlms, mpHands.HAND_CONNECTIONS)


#%%

            # Start a loop to iterate through the landmarks of the hands.
            for id, lm in enumerate(handlms.landmark):

                # Get the dimensions of the frame (height, width, and number of channels)
                h, w, c = img2.shape


            # If the index finger (4), thumb (8), middle finger (12), and pinky finger (20) are present:
            if (
                handlms.landmark[4] and
                handlms.landmark[8] and
                handlms.landmark[12] and
                handlms.landmark[20]
            ):

                # Calculate screen coordinates of the relevant landmarks
                
                #Thumb
                x1, y1 = int(handlms.landmark[4].x * w), int(handlms.landmark[4].y * h) 
                
                #Index finger
                x2, y2 = int(handlms.landmark[8].x * w), int(handlms.landmark[8].y * h)
                
                #Middle finger
                x3, y3 = int(handlms.landmark[12].x * w), int(handlms.landmark[12].y * h)
                
                #Pinky finger
                x4, y4 = int(handlms.landmark[20].x * w), int(handlms.landmark[20].y * h)


                # Calculate distances between relevant points
                
                # Calculate the distance between thumb and index finger
                distance_vol_up = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
                
                # Calculate the distance between thumb and middle finger
                distance_vol_down = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
                
                # Calculate the distance between thumb and pinky finger
                distance_pause = math.sqrt((x4 - x1)**2 + (y4 - y1)**2)

#%%

                # If the distance between thumb and pinky finger (distance_pause) is less than or equal to 45:
                if distance_pause <= 45: 
            
                    # Press the "space" key
                    pg.press("space") 
                    
                    # Wait for 0.2 seconds
                    time.sleep(0.2) 
                      
                # If the distance between thumb and index finger (distance_vol_up) is less than 30:
                elif distance_vol_up < 30: 
                    
                    # If the volume is less than 100, increase it by 2
                    if vol < 100:  
                        
                        # Increase the volume by 2
                        vol += 2  
                            
                    # Calculate volume as a ratio and limit it to a maximum of 1.0
                    volratio = min(1.0, vol / 100)  
                        
                    # Call the function to set the system volume with volratio
                    set_system_volume(volratio) 
                    
                    # Print the volume level
                    print(vol) 
                        
                
                # If the distance between thumb and middle finger (distance_vol_down) is less than 30:
                elif distance_vol_down < 30: 
                    
                    # If the volume is greater than 0, decrease it by 2
                    if vol > 0:  
                        
                        # Decrease the volume by 2
                        vol -= 2 
                            
                    
                    # Calculate volume as a ratio and limit it to a minimum of 0.0
                    volratio = max(0.0, vol / 100 )
                       
                    # Call the function to set the system volume with volratio
                    set_system_volume(volratio)
                    
                    # Print the volume level
                    print(vol)

#%%

                # Draw lines between two points (from index finger to thumb)
                cv2.line(img2, (x1, y1), (x2, y2), (255, 255, 255), 4)  

                # Draw lines between two points (from middle finger to index finger)
                cv2.line(img2, (x3, y3), (x1, y1), (255, 255, 255), 4) 

                # Draw lines between two points (from pinky finger to thumb)
                cv2.line(img2, (x4, y4), (x1, y1), (255, 255, 255), 4)  

                # Draw filled circles for index finger and thumb
                cv2.circle(img2, (x1, y1), 6, (255, 255, 0), cv2.FILLED)  # Index finger
                cv2.circle(img2, (x2, y2), 6, (255, 255, 0), cv2.FILLED)  # Thumb

                # Draw filled circles for middle finger and pinky finger
                cv2.circle(img2, (x3, y3), 6, (255, 255, 0), cv2.FILLED)  # Middle finger
                cv2.circle(img2, (x4, y4), 6, (255, 255, 0), cv2.FILLED)  # Pinky finger


#%%
    
    draw_volume_on_image(img2, vol)

    # Open a window called 'img' and display the frame in this window
    cv2.imshow("img", img2)

    # Wait for a key press and exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera source
cap.release()

# Close all windows and exit the program
cv2.destroyAllWindows()