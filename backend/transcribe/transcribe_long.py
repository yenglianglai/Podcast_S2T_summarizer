from pydub import AudioSegment
from google.cloud import speech
from dotenv import load_dotenv
import logging
import os

load_dotenv()
import wave
from google.cloud import storage

BUCKET_NAME = os.environ["BUCKET_NAME"]


def transcribe_local_mp3(mp3_audio) -> str:
    def mp3_to_wav(audio_file_name):
        logging.info("converting m3 to wav...")
        if audio_file_name.split(".")[1] == "mp3":
            sound = AudioSegment.from_mp3(audio_file_name)
            audio_file_name = audio_file_name.split(".")[0] + ".wav"
            sound.export(audio_file_name, format="wav")

    def stereo_to_mono(audio_file_name):
        sound = AudioSegment.from_wav(audio_file_name)
        sound = sound.set_channels(1)
        sound.export(audio_file_name, format="wav")

    def frame_rate_channel(audio_file_name):
        with wave.open(audio_file_name, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()
            return frame_rate, channels

    def upload_blob(bucket_name, source_file_name, destination_blob_name):
        logging.info("Uploading wav file to the bucket...")
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

    def delete_blob(bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()

    def delete_audios():
        os.remove(mp3_audio)
        os.remove(mp3_audio.replace("mp3", "wav"))

    def google_transcribe(audio_file_name):
        logging.info("Transcribing...")
        mp3_to_wav(audio_file_name)
        file_name = audio_file_name.replace("mp3", "wav")

        frame_rate, channels = frame_rate_channel(file_name)

        if channels > 1:
            stereo_to_mono(file_name)

        bucket_name = BUCKET_NAME
        source_file_name = file_name
        destination_blob_name = file_name

        upload_blob(bucket_name, source_file_name, destination_blob_name)

        gcs_uri = "gs://" + BUCKET_NAME + "/" + file_name
        transcript = ""

        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=frame_rate,
            language_code="zh-TW",
            enable_automatic_punctuation=True,
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=10000)

        for result in response.results:
            transcript += result.alternatives[0].transcript

        delete_blob(bucket_name, destination_blob_name)
        delete_audios()
        return transcript

    transcript = google_transcribe(mp3_audio)
    return transcript
