from src.llm.llm import LLMService
from src.utils.logging_utils import create_logger

logger = create_logger(__name__)


def generate_report(integrated_data, llm_service: LLMService):
    # Generate a comprehensive sentiment report
    final_prompt = """
    Generate a comprehensive sentiment report combining feedback from text, video, and audio data.
    Highlight common themes, key issues, and actionable insights.
    """
    # Assuming `model` is an instance of the LLM
    raw_response = llm_service.generate_content(
        [final_prompt, *integrated_data])
    logger.info(f"Raw Generate Report response: {raw_response}")
    response = raw_response.candidates[0].content.parts[0].text
    logger.info(f"Generate Report response: {response}")
    return response
