from src.utils.logging_utils import create_logger

logger = create_logger(__name__)


def integrate_data(outputs):
    combined_prompt = []

    for output in outputs:
        if output:
            combined_prompt.append(output)
    return combined_prompt
