import cv2
import mediapipe as mp

def track_hand():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize VideoCapture
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(rgb_frame)

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])

                # Draw a circle at the center of the hand
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_hand()