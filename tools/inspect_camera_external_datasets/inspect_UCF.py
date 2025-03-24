import os
import cv2
import random
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
DATASET_PATH = "D:/UCF101/test"  # Change this to your dataset path
SAMPLES_PER_ACTION = 2  # Adjust as needed
FRAMES_PER_VIDEO = 3  # Adjust as needed
OUTPUT_EXCEL = "camera_angles.xlsx"


def sample_frames(video_path, num_frames=3):
    """Extracts a few frames from the video."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count == 0:
        return []

    sampled_frames = sorted(random.sample(range(frame_count), min(num_frames, frame_count)))
    frames = []

    for frame_no in sampled_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for display
            frames.append((frame_no, frame))

    cap.release()
    return frames


def inspect_videos(dataset_path, samples_per_action=2, frames_per_video=3):
    results = []
    plt.figure(figsize=(12, 6))

    for action in sorted(os.listdir(dataset_path)):
        action_path = os.path.join(dataset_path, action)
        if not os.path.isdir(action_path):
            continue

        video_files = [f for f in os.listdir(action_path) if f.endswith(('.avi', '.mp4'))]
        sampled_videos = random.sample(video_files, min(samples_per_action, len(video_files)))

        for video in sampled_videos:
            video_path = os.path.join(action_path, video)
            frames = sample_frames(video_path, frames_per_video)

            for frame_no, frame in frames:
                plt.imshow(frame)
                plt.title(f"Action: {action}, Video: {video}, Frame: {frame_no}")
                plt.axis('off')
                plt.show()

                # Store results in a DataFrame for Excel
                results.append({"Action": action, "Video": video, "Frame": frame_no, "Camera Angle": ""})

    # Save to Excel
    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"Results saved to {OUTPUT_EXCEL}.")


if __name__ == '__main__':
    # Run the function
    inspect_videos(DATASET_PATH, SAMPLES_PER_ACTION, FRAMES_PER_VIDEO)
