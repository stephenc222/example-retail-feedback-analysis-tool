from src.llm.llm import LLMService
from PIL import Image
import google.generativeai as genai
import time
from src.utils.logging_utils import create_logger


class ProcessingModules:
    def __init__(self, llm_service: LLMService):
        self.llmService = llm_service
        self.logger = create_logger(__name__)

    def process_text(self, text_review):
        try:
            prompt = """Analyze the sentiment of the following reviews and summarize key themes."""
            self.logger.info("Creating prompt part...")
            self.logger.info(prompt)
            self.logger.info("Creating text reviews part...")
            self.logger.info("Generating content...")
            raw_response = self.llmService.generate_content(
                [prompt, text_review])
            response = raw_response.candidates[0].content.parts[0].text
            self.logger.info(f"Response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            return None

    def process_image(self, image: Image):
        try:
            self.logger.info("Received PIL Image object")

            # Convert bytes to Image
            self.logger.info("Converting bytes to Image...")

            prompt = """Analyze the image and generate a sentiment analysis report. Identify key topics, emotions, and significant moments."""
            self.logger.info("Generating content from image...")
            raw_response = self.llmService.generate_content(
                [prompt, image])
            response = raw_response.candidates[0].content.parts[0].text
            return response
        except Exception as e:
            self.logger.error(f"Error processing image: {e}")
            raise e

    def process_video(self, video_file_path):
        video_file = genai.upload_file(
            path=video_file_path, mime_type="video/mp4")
        while True:
            video_file = genai.get_file(video_file.name)
            if video_file.state.name != "PROCESSING":
                break
            self.logger.info('Waiting for video to be processed.')
            time.sleep(10)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)
        self.logger.info(f'Video processing complete: ' + video_file.uri)

        self.logger.info(f"Completed upload: {video_file.uri}")

        prompt = """Analyze the video testimonial and generate a sentiment analysis report. Identify key topics, emotions, and significant moments."""
        self.logger.info("Generating content from video...")

        raw_response = self.llmService.generate_content(
            [prompt, video_file])
        response = raw_response.candidates[0].content.parts[0].text
        self.logger.info(f"Video Response: {response}")
        genai.delete_file(video_file.name)

        return response

    def process_audio(self, audio_file_path):
        self.logger.info("Processing audio file...")

        audio_file = genai.upload_file(
            path=audio_file_path, mime_type="audio/wav")

        # Create a Part object from the audio bytes
        self.logger.info("Creating Part object from audio bytes...")
        prompt = """Transcribe the audio and analyze emotional tone and sentiment."""
        raw_response = self.llmService.generate_content(
            [prompt, audio_file])
        response = raw_response.candidates[0].content.parts[0].text
        self.logger.info(f"Response: {response}")
        return response
