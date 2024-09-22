import os
import ffmpeg
import tempfile
import subprocess
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class VideoIngestion:
    def preprocess_video(self, video_path):
        if not os.path.exists(video_path):
            raise FileNotFoundError(
                f"Input video file not found: {video_path}")

        # Create a temporary directory to store frames
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Get video properties
                probe = ffmpeg.probe(video_path)
                video_info = next(
                    s for s in probe['streams'] if s['codec_type'] == 'video')
                width = int(video_info['width'])
                height = int(video_info['height'])
                fps = eval(video_info['avg_frame_rate'])

                logging.info(
                    f"Video properties - Width: {width}, Height: {height}, FPS: {fps}")

                # Extract frames and apply processing
                output_pattern = os.path.join(temp_dir, 'frame%d.png')
                try:
                    (
                        ffmpeg
                        .input(video_path)
                        # .filter('colorchannelmixer', rr=0.3, rg=0.59, rb=0.11, gg=0.3, gb=0.59, gr=0.11, bb=0.3, bg=0.59, br=0.11)
                        .output(output_pattern, start_number=0)
                        .overwrite_output()
                        .run(capture_stdout=True, capture_stderr=True)
                    )
                except ffmpeg.Error as e:
                    logging.error(
                        f"Error during frame extraction: {e.stderr.decode()}")
                    raise

                # Create a list of processed frames
                frame_files = sorted([f for f in os.listdir(temp_dir) if f.startswith('frame') and f.endswith('.png')],
                                     key=lambda x: int(x[5:-4]))

                if not frame_files:
                    raise ValueError(
                        "No frames were extracted from the video.")

                # Create a temporary file for the list of frames
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as list_file:
                    for frame in frame_files:
                        list_file.write(
                            f"file '{os.path.join(temp_dir, frame)}'\n")
                    list_file_path = list_file.name

                # Define a permanent file path for the output video
                output_path = os.path.join('data', 'processed_video.mp4')

                # Combine frames into video
                try:
                    subprocess.run([
                        'ffmpeg',
                        '-y',
                        '-r', str(fps),
                        '-f', 'concat',
                        '-safe', '0',
                        '-i', list_file_path,
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        output_path
                    ], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error during video creation: {e.stderr}")
                    raise

                # Read and return the processed video file as bytes
                # with open(output_path, 'rb') as video_file:
                #     video_bytes = video_file.read()

                # Log the size of the processed video file

                return output_path

            finally:
                # Clean up temporary files
                if 'list_file_path' in locals() and os.path.exists(list_file_path):
                    os.unlink(list_file_path)
