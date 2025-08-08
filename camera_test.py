import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found.")
else:
    print("✅ Camera opened successfully. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Camera Test", frame)

    # Give enough delay for key detection
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        print("👋 Quitting camera...")
        break

cap.release()
cv2.destroyAllWindows()
