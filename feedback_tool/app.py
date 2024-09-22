from src.data_ingestion.text_ingestion import TextIngestion
from src.data_ingestion.image_ingestion import ImageIngestion
from src.data_ingestion.audio_ingestion import AudioIngestion
from src.data_ingestion.video_ingestion import VideoIngestion
from src.processing_modules import ProcessingModules
from src.data_integration import integrate_data
from src.reporting.generate_report import generate_report
from src.utils.logging_utils import create_logger
from src.utils.error_handling import *
from src.llm.llm import LLMService
import json
from src.utils.report_conversion import convert_report

from dotenv import load_dotenv
import os
load_dotenv()

# Constants for paths to media files
TEXT_SOURCE_FILE = 'text_source.txt'
IMAGE_SOURCE_FILE = 'image_source.webp'
AUDIO_SOURCE_FILE = 'audio_source.mp3'
VIDEO_SOURCE_FILE = 'video_source.mp4'

DATA_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')
JSON_REPORT_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, 'report.json')
MD_REPORT_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, 'report.md')


def main():
    logger = create_logger(__file__)

    try:
        logger.info("Starting Retail Feedback Analysis")
        # Data Ingestion
        text_ingestion = TextIngestion()
        image_ingestion = ImageIngestion()
        audio_ingestion = AudioIngestion()
        video_ingestion = VideoIngestion()
        llm_service = LLMService()
        processing_modules = ProcessingModules(llm_service)

        text_data = text_ingestion.preprocess_text(
            os.path.join(DATA_DIRECTORY_PATH, TEXT_SOURCE_FILE))
        image_path = os.path.join(DATA_DIRECTORY_PATH, IMAGE_SOURCE_FILE)

        image_data = image_ingestion.preprocess_image(image_path)
        audio_data_path = audio_ingestion.preprocess_audio(
            os.path.join(DATA_DIRECTORY_PATH, AUDIO_SOURCE_FILE))
        video_data_path = video_ingestion.preprocess_video(
            os.path.join(DATA_DIRECTORY_PATH, VIDEO_SOURCE_FILE))
        logger.info("Data ingestion completed successfully")

        # Processing
        text_output = processing_modules.process_text(text_data)
        image_output = processing_modules.process_image(image_data)
        video_output = processing_modules.process_video(video_data_path)
        audio_output = processing_modules.process_audio(audio_data_path)
        logger.info("Data processing completed successfully")

        # Integration
        integrated_data = integrate_data(
            [text_output, image_output, video_output, audio_output])
        logger.info("Data integration completed successfully")

        # Reporting
        report_md = generate_report(integrated_data, llm_service)
        logger.info("Report generation completed successfully")

        # Save report to a .md file
        with open(MD_REPORT_FILE_PATH, 'w') as md_file:
            md_file.write(report_md)
        logger.info(f"Report saved to {MD_REPORT_FILE_PATH}")

        # Convert MD report to JSON and save to a .json file
        converted_report_json = convert_report(
            report_md, llm_service, JSON_REPORT_FILE_PATH)
        logger.info(f"Converted report saved to {JSON_REPORT_FILE_PATH}")

        logger.info("Retail Feedback Analysis completed successfully")
        logger.info(json.dumps(converted_report_json, indent=4))
        logger.info(report_md)
        return converted_report_json, report_md

    except DataIngestionError as e:
        logger.error(f"Data Ingestion Error: {str(e)}")
    except PreprocessingError as e:
        logger.error(f"Preprocessing Error: {str(e)}")
    except AnalysisError as e:
        logger.error(f"Analysis Error: {str(e)}")
    except IntegrationError as e:
        logger.error(f"Integration Error: {str(e)}")
    except ReportingError as e:
        logger.error(f"Reporting Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
