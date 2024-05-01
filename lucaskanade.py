########  LUCAS KANADE #######################
import cv2
import numpy as np

# Function to calculate optical flow
def calculate_optical_flow(prev_frame, current_frame):
    # Convert frames to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow using Lucas-Kanade method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Calculate magnitude and angle of flow
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    return magnitude

# Function to detect and draw bounding boxes around aggressive motion in a video
def detect_aggressive_motion(video_path):
    # Open video capture
    cap = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, prev_frame = cap.read()

    while True:
        # Read the current frame
        ret, current_frame = cap.read()
        if not ret:
            break

        # Calculate optical flow magnitude
        magnitude = calculate_optical_flow(prev_frame, current_frame)

        # Threshold for detecting aggressive motion
        threshold = 7

        # Count the number of pixels with magnitude above the threshold
        aggressive_pixels = np.sum(magnitude > threshold)

        # If a significant number of pixels have high magnitude, consider it aggressive motion
        if aggressive_pixels > 0.02 * magnitude.size:
            print("Aggressive motion detected!")

        # Display the frame with motion information
        cv2.imshow('Video with Motion', current_frame)

        # Update the previous frame
        prev_frame = current_frame

        # Break the loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# Replace 'path/to/your/video.mp4' with the path to your video file
detect_aggressive_motion('/Users/harshi/Downloads/Abuse001_x264.mp4')
