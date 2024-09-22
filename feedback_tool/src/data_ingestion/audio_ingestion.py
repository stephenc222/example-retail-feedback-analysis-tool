import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import io
from src.utils.logging_utils import create_logger


class AudioIngestion:
    def __init__(self):
        self.logger = create_logger(__name__)

    def preprocess_audio(self, audio_path):
        try:
            # Load audio file, converting to mono
            self.logger.info(f"AUDIO PATH: {audio_path}")

            # Load and convert MP3 to WAV format using pydub
            audio = AudioSegment.from_mp3(audio_path)
            wav_path = "data/audio_source.wav"
            audio.export(wav_path, format="wav")
            self.logger.info(f"Converted to WAV: {wav_path}")

            # Load WAV audio file using librosa
            y, sr = librosa.load(wav_path, sr=None, mono=True)
            self.logger.info(
                f"Original audio shape: {y.shape}, Sample rate: {sr}")

            # Normalize audio to prevent clipping
            y = librosa.util.normalize(y)

            # Detect and handle clipping
            if np.any(y > 1.0):
                self.logger.warning("Warning: Clipping detected in audio!")

            # Resample to a consistent rate (e.g., 16kHz) if necessary
            target_sr = 16000
            if sr != target_sr:
                y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
                sr = target_sr
                self.logger.info(
                    f"Resampled audio shape: {y.shape}, New sample rate: {sr}")

            # Noise reduction
            try:
                reduced_noise_audio = nr.reduce_noise(
                    y=y, sr=sr, use_tqdm=False)
                self.logger.info(f"Noise reduction completed.")
            except Exception as e:
                self.logger.warning(f"Noise reduction failed: {e}")
                reduced_noise_audio = y  # Fallback to original audio

            # Check for NaNs or Infs in the reduced noise audio
            if np.isnan(reduced_noise_audio).any():
                self.logger.warning(
                    "Warning: NaN values found in reduced noise audio!")
                reduced_noise_audio = np.nan_to_num(reduced_noise_audio)

            if np.isinf(reduced_noise_audio).any():
                self.logger.warning(
                    "Warning: Infinity values found in reduced noise audio!")
                reduced_noise_audio = np.nan_to_num(reduced_noise_audio)

            # Convert to float32 for encoding
            reduced_noise_audio = reduced_noise_audio.astype(np.float32)

            # Save the processed audio as a new WAV file for validation
            processed_wav_path = "data/processed_audio.wav"
            sf.write(processed_wav_path, reduced_noise_audio, sr)
            self.logger.info(f"Processed audio saved to: {processed_wav_path}")

            # Convert audio to bytes
            with io.BytesIO() as output:
                sf.write(output, reduced_noise_audio, sr, format='WAV')
                audio_bytes = output.getvalue()

            # Pass the audio bytes to process_audio in processing_modules.py
            self.logger.info(f"Audio bytes: {len(audio_bytes)}")

            return processed_wav_path
        except Exception as e:
            self.logger.error(f"Error during audio preprocessing: {e}")
            return None


# Usage Example
# audio_ingestion = AudioIngestion()
# encoded_audio = audio_ingestion.preprocess_audio("path/to/audio/file.wav")
