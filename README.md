 Installation Instructions
1. Clone the Repository
git clone https://github.com/<your-username>/video-reconstruction.git
cd video-reconstruction
2. Install Dependencies
Ensure you have Python 3.8+ installed. Then install the following required libraries 
opencv-python
numpy
tqdm
pip install opencv-python numpy tqdm

Running the Code
1. Place the Jumbled Video
Save your jumbled video file. and add its path in the code
2. Run the Script
Execute the following command in your terminal:
python tech.py
3. Output
The reconstructed video will be saved as:
reconstructed_final.mp4
Testing the Algorithm
1. Using the Provided Evaluation Video
   put the path to the video in code
   run
python tech.py
2. Checking the Results
You can visually inspect continuity and transitions to confirm that the frames flow naturally.


Algorithm Explanation
The goal of this project was to reconstruct a 10-second jumbled video (30 frames per second, approximately 300 frames) back into its original chronological order.
Since the frames were randomly shuffled and no metadata such as timestamps or sequence numbers was available, the reconstruction process relied entirely on the intrinsic visual similarity between frames.
The design of the algorithm followed a structured, multi-step approach that combined frame similarity measurement, greedy sequence ordering, local refinement, and final sequence validation to achieve the most natural and smooth temporal flow possible in the reconstructed video.
To estimate the degree of visual similarity between frames, each frame was first converted to grayscale. 
This step was crucial for simplifying the computation by reducing the amount of data processed per frame while still preserving important spatial and structural details. 
The algorithm then used the Mean Squared Error (MSE) as its primary similarity metric, a mathematically straightforward yet effective measure for comparing image intensity patterns.
A smaller MSE value indicates a higher degree of similarity, suggesting that the two frames are likely adjacent in the original timeline.
Using this principle, the algorithm computed an NxN difference matrix, where each element represented the MSE value between a pair of frames.
This matrix effectively captured the global visual relationships within the video and served as the foundation for reconstructing the correct frame order.
Once the difference matrix was established, the algorithm identified a starting frame — specifically, the one least similar to all others based on average MSE — since it likely corresponded to either the very beginning or the end of the video. 
From this point, a greedy reconstruction strategy was employed: at each iteration, the algorithm selected the most visually similar unvisited frame to the current frame and appended it to the sequence. 
This approach allowed the system to build a near-optimal sequence in a data-driven manner without requiring any prior knowledge of the content or the use of pretrained machine learning models. 
The greedy method was particularly well-suited for this task as it balances computational feasibility with a reasonable level of reconstruction accuracy.
After producing the initial frame order, the algorithm performed a local refinement phase to enhance visual continuity.
This step analyzed consecutive triplets of frames and swapped adjacent frames when doing so resulted in smoother transitions, thereby reducing abrupt changes in motion or brightness between frames.
To further ensure correct temporal direction, a continuity verification stage was introduced.
The algorithm computed a total discontinuity score for both the forward and reversed versions of the reconstructed sequence.
The version with the lower overall discontinuity was chosen as the final output, ensuring that the reconstructed video followed the natural progression of movement and scene evolution.
This approach was selected primarily for its simplicity, interpretability, and efficiency.
Unlike AI-based models that require extensive labeled datasets and high computational resources, the MSE-based similarity method is transparent, lightweight, and easily adaptable to different types of videos.
It provides an ideal balance between performance and accuracy, especially for short-duration clips. 
The algorithm’s time complexity is O(N²), dominated by the pairwise frame comparison step, which remains computationally feasible for videos under a few hundred frames. 
The implementation also emphasizes reproducibility, featuring detailed runtime logs, timestamps, and progress tracking through the tqdm progress bar.
These design considerations make the system both traceable and easy to evaluate.
In summary, the video reconstruction pipeline consists of several clearly defined stages — frame extraction, grayscale conversion, MSE-based similarity computation, greedy sequence reconstruction, refinement for local continuity, forward/reverse validation, and output generation. 
Together, these components form a heuristic yet highly effective framework for restoring the temporal coherence of a jumbled video. 
The algorithm demonstrates that even with simple statistical measures and logical sequencing, it is possible to achieve a visually smooth, accurate reconstruction while maintaining computational efficiency, transparency, and robustness.

Execution Time Log
[20:48:44] Video Reconstruction Log
[20:48:44] Input file: /Users/yashikagupta/Downloads/jumbled_video.mp4
[20:48:44] Output file: reconstructed_final.mp4
[20:48:44] FPS: 30
[20:48:44] Video metadata - Total frames: 300, Resolution: 1920x1080
[20:48:44] Reading frames...
[20:48:45] All 300 frames extracted successfully in 0.73s.
[20:48:45] Converted frames to grayscale in 0.32s.
[20:48:45] Computing frame-to-frame differences...
[20:50:36] Frame difference map computed in 110.80s.
[20:50:36] Estimated starting frame index: 0
[20:50:36] Initial reconstruction order generated in 0.00s.
[20:50:37] Sequence refinement completed in 1.48s.
[20:50:39] Reversed sequence chosen for smoother continuity.
[20:50:42] Output video written successfully in 2.95s.
[20:50:42] Total reconstruction time: 1.96 minutes (117.76 seconds).
