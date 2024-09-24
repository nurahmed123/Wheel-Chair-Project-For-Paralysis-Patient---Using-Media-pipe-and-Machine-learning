import cv2
import mediapipe as mp
import requests

# নোড MCU বোর্ড এর ঠিকানা
ESP8266_IP = "http://192.168.230.85"


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


mp_draw = mp.solutions.drawing_utils

# নির্দেশ সমূহ
commands = {
    'forward': 'both/forward',
    'backward': 'both/backward',
    'left': 'turn_left',
    'right': 'turn_right',
    'stop': 'stop'
}

# অঙ্গভঙ্গি নিয়ন্ত্রণ variables
control_on = False  
last_command = None  
closed_fist_threshold = 0.1


cap = cv2.VideoCapture(0)

# ভিডিও ধারণ পুণ:নিরীক্ষণ
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

def send_command(command):
    
    url = f"{ESP8266_IP}/{command}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command '{command}' sent successfully")
        else:
            print(f"Failed to send command '{command}'")
    except Exception as e:
        print(f"Error sending command: {e}")

while True:
    ret, frame = cap.read()
    
   # ফ্রেম যাচাই
    if not ret:
        print("Failed to capture image.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

     # হাতের সীমারেখা নির্ণয়
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # অঙ্গভঙ্গি যাচাই এর জন্য revelant সীমারেখা
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            
            thumb_index_dist = abs(thumb_tip.y - index_tip.y)
            command = "stop"  # Default 

            
            if thumb_index_dist < closed_fist_threshold:
                command = "stop"

           
            elif index_tip.y < thumb_tip.y and middle_tip.y < thumb_tip.y:
                command = "forward"

            
            elif index_tip.y > thumb_tip.y and middle_tip.y > thumb_tip.y:
                command = "backward"

            
            elif index_tip.x < thumb_tip.x:
                command = "left"

            
            elif index_tip.x > thumb_tip.x:
                command = "right"

            if command != last_command:
                send_command(commands[command])
                last_command = command

            # Draw 
            cv2.putText(frame, command.capitalize(), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Control', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()