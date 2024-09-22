# from src.llm.llm import Part
from src.utils.logging_utils import create_logger

logger = create_logger(__name__)


def integrate_data(outputs):
    # Combine all outputs into one prompt of VertexAI Parts as text
    combined_prompt = []

    for output in outputs:
        if output:
            logger.info(f"Creating text part from output")
            combined_prompt.append(output)
    return combined_prompt
