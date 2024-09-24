# Retail Feedback Analysis

## Setup

1. **Clone the repository:**

   ```sh
   git clone git@github.com:stephenc222/example-retail-feedback-analysis-tool.git
   cd example-retail-feedback-analysis-tool
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   - Create a `.env` file in the root directory of the project.
   - Copy the contents of `.env.example` into `.env` and fill in your Google API key.
   - Need to setup a Google GenAI billing account

5. **Generate a report:**

   ```sh
   sh generate_report.sh
   ```

6. **Build the client:**

   ```sh
   sh build_client.sh
   ```

7. **Start the Flask app:**

   ```sh
   sh start_server.sh
   ```

After the Flask app is running, you can access the client at `http://localhost:5000`.

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

## Error Handling

Custom exceptions are used throughout the codebase to handle specific errors in data ingestion, preprocessing, analysis, integration, and reporting steps.
