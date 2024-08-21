# the script is for embedding text and video by towhee, and then calculate the similarity of the text and video.
# pip install ffmpeg-python==0.2.0 imageio-ffmpeg==0.4.9 pytorchvideo==0.1.5 torch==2.4.0 torchvision==0.19.0 towhee==1.1.3 towhee.models==1.1.3
# for pytorchvideo, should fix site-packages/pytorchvideo/transforms/augmentations.py by (for affine() function calling):
#import torchvision.transforms.functional_tensor as F_t
# ---> 
#import torchvision.transforms.functional as F_t

import os
import towhee
import numpy as np
from towhee import pipe, ops, DataCollection

# Function to calculate cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Text to compare
text = "eating"
video_path = "/Users/david/videos/abcd.mp4"

# Video embedding pipeline
# uniform_temporal_subsample:
# selects a predetermined number of evenly separated frames over the duration of the clip
video_pipe = (
    pipe.input('video_path')
        .map('video_path', 'flame_gen', ops.video_decode.ffmpeg(sample_type='uniform_temporal_subsample', args={'num_samples': 10}))
        .map('flame_gen', 'flame_list', lambda x: [y for y in x])
        .map('flame_list', 'vec', ops.video_text_embedding.frozen_in_time(model_name='frozen_in_time_base_16_244', modality='video', device='mps'))
        .output('video_path', 'flame_list', 'vec')
)

# Text embedding pipeline
text_pipe = (
    pipe.input('text')
        .map('text', 'vec', ops.video_text_embedding.frozen_in_time(model_name='frozen_in_time_base_16_244', modality='text', device='mps'))
        .output('text', 'vec')
)

#DataCollection(p('kids feeding and playing with the horse')).show()

def text_video_similarity(video_path:str, text:str):
    # Get video embedding
    video_result = DataCollection(video_pipe(video_path)).to_list()[0]
    video_embedding = video_result['vec']

    # Get text embedding
    text_result = DataCollection(text_pipe(text)).to_list()[0]
    text_embedding = text_result['vec']

    # Calculate cosine similarity between text and video embeddings
    return cosine_similarity(text_embedding, video_embedding)


video_folder = '/Users/david/videos/swimming/'
input_text = 'swimming'

# similarity = text_video_similarity(video_path, text)
# print(f"Similarity between text and video: {similarity}")

# Loop through each video file in the video_folder recursively
video_similarities = []
for root, dirs, files in os.walk(video_folder):
    for file in files:
        if file.endswith(('.mp4', '.avi', '.mov')):  # Adjust file extensions as needed
            video_path = os.path.join(root, file)
            similarity = text_video_similarity(video_path, input_text)
            video_similarities.append((video_path, similarity))

# Sort the results by similarity in ascending order
video_similarities.sort(key=lambda x: x[1])

# Print each video path with the similarity score
for video_path, similarity in video_similarities:
    print(f"Video: {video_path}, Similarity: {similarity}")
