import os
import cv2
import random
import pandas as pd
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Configuration
DATASET_PATH = "D:/UCF101/test"  # Change to your dataset path
SAMPLES_PER_ACTION = 6  # Adjust as needed
FRAMES_PER_VIDEO = 1  # Adjust as needed
MIN_VOTES_THRESHOLD = 2  # Minimum votes for an angle to be considered relevant
OUTPUT_EXCEL = "camera_angle_results.xlsx"
SUMMARY_EXCEL = "camera_angle_summary.xlsx"

# Initialize MediaPipe Pose detector
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()


def delete_existing_files():
    """Deletes previous Excel files if they exist to prevent outdated data."""
    for file in [OUTPUT_EXCEL, SUMMARY_EXCEL]:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted existing file: {file}")


def detect_camera_angle(frame):
    """Analyze the frame to determine camera angle"""
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if not results.pose_landmarks:
        return "No person detected", None

    keypoints = results.pose_landmarks.landmark

    # Get bounding box of the detected body (approximate)
    x_coords = [kp.x for kp in keypoints]
    y_coords = [kp.y for kp in keypoints]

    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)

    bbox_width = (xmax - xmin) * w
    bbox_height = (ymax - ymin) * h

    # Define camera angle rules
    if bbox_width > 0.7 * w and bbox_height > 0.7 * h:
        return "Close-up (face or hands)", results
    elif bbox_width > 0.6 * w and ymin < 0.2:  # Face near the top of the frame
        return "Face-only close-up", results
    elif bbox_width > 0.5 * w and bbox_height > 0.5 * h:
        return "Upper body shot (partially visible person)", results
    elif ymin > 0.3 and ymax < 0.9:  # Hands prominent in front
        return "1st person (hands-focused)", results
    elif bbox_width < 0.4 * w and bbox_height < 0.5 * h:
        return "3rd person (far away)", results
    else:
        return "Mixed/Unknown", results


def draw_pose_on_frame(frame, results):
    """Draw detected pose landmarks on the frame"""
    frame_copy = frame.copy()
    frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)

    if results and results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    return frame_rgb


def process_videos(dataset_path, samples_per_action=2, frames_per_video=3):
    results = []

    for action in sorted(os.listdir(dataset_path)):
        action_path = os.path.join(dataset_path, action)
        if not os.path.isdir(action_path):
            continue

        video_files = [f for f in os.listdir(action_path) if f.endswith(('.avi', '.mp4'))]
        sampled_videos = random.sample(video_files, min(samples_per_action, len(video_files)))

        for video in sampled_videos:
            video_path = os.path.join(action_path, video)
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if frame_count == 0:
                continue

            sampled_frames = sorted(random.sample(range(frame_count), min(frames_per_video, frame_count)))

            for frame_no in sampled_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()
                if not ret:
                    continue

                # Detect camera angle and pose
                angle, pose_results = detect_camera_angle(frame)

                # Ignore frames where pose is not detected or is uncertain
                if angle in ["Mixed/Unknown", "No person detected"]:
                    continue

                # Draw pose on frame
                frame_with_pose = draw_pose_on_frame(frame, pose_results)

                # Save only valid frames
                results.append({"Action": action, "Video": video, "Frame": frame_no, "Detected Camera Angle": angle})

                # Show frame with pose overlay
                plt.figure(figsize=(6, 4))
                plt.imshow(frame_with_pose)
                plt.title(f"Action: {action} | Angle: {angle}")
                plt.axis('off')
                plt.show(block=False)

                # Wait for key press to proceed
                # input("Press Enter to continue to the next frame...")
                plt.close()

            cap.release()

    # Save only valid detections to Excel
    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"Results saved to {OUTPUT_EXCEL}.")

    # Create clustered summary
    create_summary_excel(df)


def create_summary_excel(df):
    """Create an aggregated Excel file with the most relevant camera angles for each action"""
    if df.empty:
        print("No valid detections found, skipping summary creation.")
        return

    summary_results = []
    all_actions = sorted([name for name in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, name))])

    # Manually aggregate counts instead of relying on groupby
    action_groups = df.groupby("Action")
    for action in all_actions:
        if action in action_groups.groups:
            group = action_groups.get_group(action)
            angle_counts = group["Detected Camera Angle"].value_counts().to_dict()

            # Filter out angles that have fewer than MIN_VOTES_THRESHOLD
            filtered_angles = {
                angle: count for angle, count in angle_counts.items() if count >= MIN_VOTES_THRESHOLD
            }

            # If filtering removes everything, just take the top 1-2 most common angles
            if not filtered_angles:
                filtered_angles = dict(sorted(angle_counts.items(), key=lambda x: x[1], reverse=True)[:2])

            angle_summary = ", ".join([f"{angle} ({count})" for angle, count in filtered_angles.items()])
        else:
            angle_summary = "Unknown"

        summary_results.append({"Action": action, "Most Frequent Camera Angles": angle_summary})

    # Save summary to Excel
    summary_df = pd.DataFrame(summary_results)
    summary_df.to_excel(SUMMARY_EXCEL, index=False)
    print(f"Summary saved to {SUMMARY_EXCEL}.")


if __name__ == '__main__':
    # Clear previous results
    delete_existing_files()

    # Run the function
    process_videos(DATASET_PATH, SAMPLES_PER_ACTION, FRAMES_PER_VIDEO)
