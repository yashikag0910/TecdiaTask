import cv2
import numpy as np
from tqdm import tqdm

# Input and output video file paths
input_path = "/Users/yashikagupta/Downloads/jumbled_video.mp4"
output_path = "reconstructed_final.mp4"
fps = 30  # Frames per second for the output video

# Open the input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise ValueError("Unable to open input video.")

# Get video metadata
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Read all frames from the input video
frames = []
print(f"Reading {total_frames} frames")
for _ in tqdm(range(total_frames)):
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()
print("All frames extracted successfully.")

# Convert all frames to grayscale for easier comparison
gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

# Function to compute mean squared error (MSE) between two frames
def frame_diff(a, b):
    return np.mean((a.astype("float") - b.astype("float")) ** 2)

# Compute similarity (difference) between every pair of frames
print("Analyzing frame-to-frame differences")
n = len(gray)
difference_map = np.zeros((n, n))

for i in tqdm(range(n)):
    for j in range(i + 1, n):
        diff_value = frame_diff(gray[i], gray[j])
        difference_map[i, j] = diff_value
        difference_map[j, i] = diff_value

# Set diagonal to infinity (a frame compared with itself)
np.fill_diagonal(difference_map, np.inf)

# Choose the starting frame — the one least similar to all others
avg_diffs = np.mean(difference_map, axis=1)
starting_index = np.argmax(avg_diffs)
print(f"Starting frame estimated at index: {starting_index}")

# Build a greedy reconstruction order
visited = {starting_index}
reconstructed_order = [starting_index]

for _ in tqdm(range(n - 1)):
    last_idx = reconstructed_order[-1]
    next_idx = np.argmin(difference_map[last_idx])
    # Avoid reusing already visited frames
    while next_idx in visited:
        difference_map[last_idx, next_idx] = np.inf
        next_idx = np.argmin(difference_map[last_idx])
    reconstructed_order.append(next_idx)
    visited.add(next_idx)

# Minor smoothing to correct misplaced neighboring frames
def refine_sequence(order_list, gray_frames):
    optimized = order_list.copy()
    for i in range(1, len(order_list) - 1):
        prev_f = gray_frames[optimized[i - 1]]
        curr_f = gray_frames[optimized[i]]
        next_f = gray_frames[optimized[i + 1]]
        # If skipping the current frame gives smoother continuity, swap
        if frame_diff(prev_f, next_f) < frame_diff(prev_f, curr_f):
            optimized[i], optimized[i + 1] = optimized[i + 1], optimized[i]
    return optimized

reconstructed_order = refine_sequence(reconstructed_order, gray)

# Measure continuity to decide forward or reversed order
def total_discontinuity(order_list):
    score = 0
    for i in range(1, len(order_list)):
        score += frame_diff(gray[order_list[i - 1]], gray[order_list[i]])
    return score

# Compute continuity scores for forward and reversed sequence
forward_cost = total_discontinuity(reconstructed_order)
reverse_cost = total_discontinuity(reconstructed_order[::-1])

# Choose the smoother direction
if reverse_cost < forward_cost:
    reconstructed_order = reconstructed_order[::-1]
    print("Reversing frame sequence for smoother continuity.")
else:
    print("Keeping forward order for better continuity.")

# Write the reconstructed video
print("Writing output video")
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

for idx in reconstructed_order:
    writer.write(frames[idx])
writer.release()

print(f"Final reconstructed video saved as {output_path}")
