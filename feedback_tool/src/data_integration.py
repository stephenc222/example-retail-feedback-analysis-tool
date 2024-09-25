from typing import List
from src.utils.logging_utils import create_logger

logger = create_logger(__name__)


def integrate_data(outputs: List[str]) -> List[str]:
    """
    Integrate the non-empty outputs into a combined list.

    Args:
        outputs (List[str]): A list of output strings to be integrated.

    Returns:
        List[str]: A list of non-empty output strings.
    """
    combined_prompt = [output for output in outputs if output]
    logger.info(f"Data integration complete. Combined {len(combined_prompt)} non-empty outputs.")
    return combined_prompt
