# Retail Feedback Analysis

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-repo/retail-feedback-analysis.git
   cd retail-feedback-analysis
   ```

2. Cd into the feedback_tool directory

   ```sh
   cd feedback_tool
   ```

3. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**

   - Create a `.env` file in the root directory of the project.
   - Copy the contents of `.env.example` into `.env` and fill in your Google API key.
   - Need to setup a Google GenAI billing account

6. **Run the application:**
   ```sh
   python app.py
   ```

## Dependencies

- Python 3.8+
- `google-generativeai`
- `dotenv`
- `ffmpeg-python`
- `librosa`
- `noisereduce`
- `numpy`
- `soundfile`
- `pydub`
- `spacy`
- `opencv-python`
- `Pillow`

## Additional Setup

- Install ffmpeg if not already installed:
  ```sh
  pip install ffmpeg-python
  ```

## Logging

Logs are stored in the `logs` directory. Ensure this directory exists or is created by the application.

## Error Handling

Custom exceptions are used throughout the codebase to handle specific errors in data ingestion, preprocessing, analysis, integration, and reporting steps.
