import json
from src.llm.llm import LLMService
from src.utils.logging_utils import create_logger

logger = create_logger(__name__)

# JSON Schema for the report
report_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sentiment Analysis Report",
    "description": "Schema for a sentiment analysis report on a malfunctioning coffee maker",
    "type": "object",
    "properties": {
        "themes": {
            "description": "List of themes identified in the analysis",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "description": "Name of the theme",
                        "type": "string"
                    },
                    "description": {
                        "description": "Description of the theme",
                        "type": "string"
                    }
                },
                "required": ["name", "description"]
            }
        },
        "issues": {
            "description": "List of issues identified in the analysis",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "description": "Name of the issue",
                        "type": "string"
                    },
                    "description": {
                        "description": "Description of the issue",
                        "type": "string"
                    }
                },
                "required": ["name", "description"]
            }
        },
        "insights": {
            "description": "List of insights and recommendations based on the analysis",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "Unique identifier for the insight",
                        "type": "integer"
                    },
                    "recommendation": {
                        "description": "Recommendation based on the insight",
                        "type": "string"
                    },
                    "reason": {
                        "description": "Reason for the recommendation",
                        "type": "string"
                    }
                },
                "required": ["id", "recommendation", "reason"]
            }
        },
        "metadata": {
            "description": "Metadata about the report",
            "type": "object",
            "properties": {
                "report_title": {
                    "description": "Title of the report",
                    "type": "string"
                },
                "overall_sentiment": {
                    "description": "Overall sentiment derived from the analysis",
                    "type": "string"
                },
                "sentiment_description": {
                    "description": "Description of the overall sentiment",
                    "type": "string"
                }
            },
            "required": ["report_title", "overall_sentiment", "sentiment_description"]
        }
    },
    "required": ["themes", "issues", "insights", "metadata"]
}


def convert_report(md_report: str, llm_service: LLMService, output_file_path: str):
    # Define the prompt for the LLM
    prompt = f"""
    Convert the following Markdown report to a raw JSON string format:
    
    {md_report}
    
    Provide the JSON with keys: 'themes', 'issues', 'insights', and 'metadata'.
    Ensure the output is a raw JSON string without any markdown syntax demarcation.
    
    The JSON should conform to the following schema:
    {json.dumps(report_schema, indent=4)}
    """

    # Generate the JSON report using the LLM
    raw_response = llm_service.generate_content([prompt])
    logger.info(f"Raw Convert Report response: {raw_response}")
    response = raw_response.candidates[0].content.parts[0].text
    logger.info(f"Convert Report response: {response}")

    # Parse the response as JSON
    report_json = json.loads(response)

    # Save the JSON report to a file
    with open(output_file_path, 'w') as json_file:
        json.dump(report_json, json_file, indent=4)
    logger.info(f"Converted report saved to {output_file_path}")

    return report_json
