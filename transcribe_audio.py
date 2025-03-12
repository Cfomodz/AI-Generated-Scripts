import speech_recognition as sr
import json
from pydub import AudioSegment
import os

def transcribe_audio_segments(audio_file, segment_length_ms=30000, overlap_ms=5000):
    """
    Transcribe audio file in segments with timestamps
    
    Args:
        audio_file: Path to the audio file
        segment_length_ms: Length of each segment in milliseconds
        overlap_ms: Overlap between segments in milliseconds
    
    Returns:
        List of dictionaries with start_time, end_time, and text
    """
    # Load the audio file
    print(f"Loading audio file: {audio_file}")
    audio = AudioSegment.from_wav(audio_file)
    
    # Get the duration of the audio file
    duration_ms = len(audio)
    print(f"Audio duration: {duration_ms/1000:.2f} seconds")
    
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Initialize the list to store transcriptions
    transcriptions = []
    
    # Process the audio in segments
    start_ms = 0
    segment_count = 0
    
    while start_ms < duration_ms:
        segment_count += 1
        print(f"Processing segment {segment_count}: {start_ms/1000:.2f}s to {min((start_ms + segment_length_ms)/1000, duration_ms/1000):.2f}s")
        
        # Extract the segment
        end_ms = min(start_ms + segment_length_ms, duration_ms)
        segment = audio[start_ms:end_ms]
        
        # Export the segment to a temporary file
        temp_segment_path = f"/tmp/segment_{segment_count}.wav"
        segment.export(temp_segment_path, format="wav")
        
        # Transcribe the segment
        try:
            with sr.AudioFile(temp_segment_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                
                if text:
                    transcriptions.append({
                        "start_time": start_ms / 1000,  # Convert to seconds
                        "end_time": end_ms / 1000,      # Convert to seconds
                        "text": text
                    })
                    print(f"Transcribed: {text[:50]}...")
        except Exception as e:
            print(f"Error transcribing segment {segment_count}: {e}")
        
        # Remove the temporary file
        os.remove(temp_segment_path)
        
        # Move to the next segment with overlap
        start_ms += segment_length_ms - overlap_ms
    
    return transcriptions

def save_transcriptions(transcriptions, output_file):
    """Save transcriptions to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(transcriptions, f, indent=2)
    print(f"Transcriptions saved to {output_file}")

if __name__ == "__main__":
    audio_file = "/home/ubuntu/upload/DeepSeek-R1-Podcast.wav"
    output_file = "/home/ubuntu/podcast_project/transcriptions.json"
    
    # Transcribe the audio
    transcriptions = transcribe_audio_segments(audio_file)
    
    # Save the transcriptions
    save_transcriptions(transcriptions, output_file)
