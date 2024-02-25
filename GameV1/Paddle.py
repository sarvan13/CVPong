import cv2
import mediapipe as mp

class Paddle:
    def __init__(self, y, speed):
        self.y = y
        self.speed = speed

    def getPlayerPaddle(self, frame, mp_hands, hands):
        results = hands.process(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the center of the hand
                cx, cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * frame.shape[1]), \
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * frame.shape[0])
                
                self.speed = cy - self.y
                self.y = cy

                # Draw a circle at the center of the hand
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)