# Kushagra Darji (IHackAWS Hackathon Task)

import boto3
from botocore.exceptions import NoCredentialsError
import json
import cv2
import librosa
import numpy as np

rekognition_client = boto3.client('rekognition')
transcribe_client = boto3.client('transcribe')

def analyze_call_transcript(audio_file):
    """Analyze call transcripts for phishing or scam patterns."""
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName='TranscribeJob',
            Media={'MediaFileUri': audio_file},
            MediaFormat='mp4',
            LanguageCode='en-US'
        )
        transcript = response['Transcript']['TranscriptFileUri']
        fraud_keywords = ["transfer", "OTP", "password"]
        if any(keyword in transcript for keyword in fraud_keywords):
            return "Potential Scam Detected"
        return "Clean Call"
    except NoCredentialsError:
        print("AWS Credentials not found!")
        return None

def detect_deepfake(video_file):
    """Detect deepfake in video using Rekognition."""
    with open(video_file, 'rb') as video:
        response = rekognition_client.detect_faces(
            Video={'Bytes': video.read()},
            Attributes=['ALL']
        )
        for faceDetail in response['FaceDetails']:
            if faceDetail['Confidence'] < 70:  
                return "Deepfake Detected"
        return "Authentic Video"

def monitor_transactions(transactions):
    """Monitor transactions for anomalies."""
    for txn in transactions:
        if txn['amount'] > 100000 or "multiple small transactions":
            return "Suspicious Activity Detected"
    return "No Anomalies"

audio_file = "s3://your-audio-file.mp4"
video_file = "path/to/video.mp4"
transactions = [{"amount": 150000, "type": "wire transfer"}]

call_analysis = analyze_call_transcript(audio_file)
deepfake_analysis = detect_deepfake(video_file)
transaction_analysis = monitor_transactions(transactions)

print(f"Call Analysis: {call_analysis}")
print(f"Deepfake Analysis: {deepfake_analysis}")
print(f"Transaction Analysis: {transaction_analysis}")
