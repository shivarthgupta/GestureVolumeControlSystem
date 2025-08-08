import cv2
import mediapipe as mp
import math
import subprocess

# Mediapipe setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

def set_volume_mac(volume_percent):
    """Set system volume on macOS (0-100)"""
    volume_percent = max(0, min(100, int(volume_percent)))
    subprocess.call(["osascript", "-e", f"set volume output volume {volume_percent}"])

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Get landmark positions
            lmList = []
            h, w, _ = img.shape
            for id, lm in enumerate(handLms.landmark):
                lmList.append((int(lm.x * w), int(lm.y * h)))

            # Thumb tip (id=4) and index finger tip (id=8)
            x1, y1 = lmList[4]
            x2, y2 = lmList[8]

            # Draw line and circle
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), -1)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), -1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Distance between fingers
            length = math.hypot(x2 - x1, y2 - y1)

            # Map length to volume range (20 to 200 px → 0 to 100%)
            vol = int(((length - 20) / (200 - 20)) * 100)
            vol = max(0, min(100, vol))

            set_volume_mac(vol)

            # Show volume level
            cv2.putText(img, f'Vol: {vol}%', (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Gesture Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
