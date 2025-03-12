import json
from pydub import AudioSegment
import os

def select_best_segments(transcriptions_file, total_duration=120):
    """
    Select the best segments for the highlight reel
    
    Args:
        transcriptions_file: Path to the transcriptions JSON file
        total_duration: Target duration in seconds
    
    Returns:
        List of selected segments
    """
    # Load transcriptions
    with open(transcriptions_file, 'r') as f:
        transcriptions = json.load(f)
    
    # Select the most interesting segments based on content
    # These are manually selected based on content quality and narrative flow
    selected_indices = [0, 1, 6, 10, 11, 12, 14, 15]
    
    selected_segments = [transcriptions[i] for i in selected_indices]
    
    return selected_segments

def extract_audio_segments(input_file, selected_segments, output_dir):
    """
    Extract selected segments from the original audio file
    
    Args:
        input_file: Path to the original audio file
        selected_segments: List of selected segments
        output_dir: Directory to save extracted segments
    
    Returns:
        List of extracted segment files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the original audio file
    original_audio = AudioSegment.from_wav(input_file)
    
    extracted_files = []
    
    for i, segment in enumerate(selected_segments):
        # Extract segment
        start_ms = segment["start_time"] * 1000
        end_ms = segment["end_time"] * 1000
        audio_segment = original_audio[start_ms:end_ms]
        
        # Save segment
        output_file = f"{output_dir}/highlight_{i+1}.wav"
        audio_segment.export(output_file, format="wav")
        
        extracted_files.append({
            "file": output_file,
            "start_time": segment["start_time"],
            "end_time": segment["end_time"],
            "text": segment["text"]
        })
        
        print(f"Extracted segment {i+1}: {segment['text'][:50]}...")
    
    return extracted_files

if __name__ == "__main__":
    input_file = "/home/ubuntu/upload/DeepSeek-R1-Podcast.wav"
    transcriptions_file = "/home/ubuntu/podcast_project/transcriptions.json"
    output_dir = "/home/ubuntu/podcast_project/highlights"
    
    # Select best segments
    print("Selecting best segments...")
    selected_segments = select_best_segments(transcriptions_file)
    
    # Extract audio segments
    print("Extracting audio segments...")
    extracted_files = extract_audio_segments(input_file, selected_segments, output_dir)
    
    # Save selected segments info
    with open("/home/ubuntu/podcast_project/selected_segments.json", 'w') as f:
        json.dump(extracted_files, f, indent=2)
    
    print(f"Extracted {len(extracted_files)} segments for the highlight reel")
