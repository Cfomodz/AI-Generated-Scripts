import speech_recognition as sr
from pydub import AudioSegment
import json
import os
import time

def extract_segments_with_ffmpeg(input_file, output_dir):
    """Extract 10-second segments from the audio file using ffmpeg"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract segments at different positions throughout the file
    # Targeting positions that are likely to contain complete thoughts
    positions = [30, 90, 150, 210, 270, 330, 390, 450, 510, 570, 630, 690, 750, 810, 870, 930]
    segment_files = []
    
    for i, pos in enumerate(positions):
        output_file = f"{output_dir}/segment_{i+1}.wav"
        # Extract 15-second segment starting at position
        os.system(f"ffmpeg -i {input_file} -ss {pos} -t 15 -c copy {output_file} -y -v quiet")
        segment_files.append({
            "file": output_file,
            "start_time": pos,
            "end_time": pos + 15
        })
    
    return segment_files

def transcribe_segments(segment_files):
    """Transcribe each segment and return with timestamps"""
    recognizer = sr.Recognizer()
    transcriptions = []
    
    for segment in segment_files:
        try:
            with sr.AudioFile(segment["file"]) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                
                if text:
                    transcriptions.append({
                        "start_time": segment["start_time"],
                        "end_time": segment["end_time"],
                        "text": text,
                        "file": segment["file"]
                    })
                    print(f"Segment {segment['start_time']}s-{segment['end_time']}s: {text[:100]}...")
        except Exception as e:
            print(f"Error transcribing segment {segment['file']}: {e}")
    
    return transcriptions

def save_transcriptions(transcriptions, output_file):
    """Save transcriptions to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(transcriptions, f, indent=2)
    print(f"Transcriptions saved to {output_file}")

if __name__ == "__main__":
    input_file = "/home/ubuntu/upload/DeepSeek-R1-Podcast.wav"
    output_dir = "/home/ubuntu/podcast_project/segments"
    output_file = "/home/ubuntu/podcast_project/transcriptions.json"
    
    # Extract segments
    print("Extracting segments...")
    segment_files = extract_segments_with_ffmpeg(input_file, output_dir)
    
    # Transcribe segments
    print("Transcribing segments...")
    transcriptions = transcribe_segments(segment_files)
    
    # Save transcriptions
    save_transcriptions(transcriptions, output_file)
    
    print("Done!")
