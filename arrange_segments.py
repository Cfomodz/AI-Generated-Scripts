import json
from pydub import AudioSegment
import os

def arrange_segments(segments_file, output_file, crossfade_duration=500):
    """
    Arrange segments with smooth transitions
    
    Args:
        segments_file: Path to the selected segments JSON file
        output_file: Path to save the arranged audio file
        crossfade_duration: Crossfade duration in milliseconds
    
    Returns:
        Total duration of the arranged audio
    """
    # Load segments info
    with open(segments_file, 'r') as f:
        segments = json.load(f)
    
    # Initialize the combined audio
    combined = AudioSegment.empty()
    
    # Add segments with crossfade
    for i, segment in enumerate(segments):
        # Load segment audio
        segment_audio = AudioSegment.from_wav(segment["file"])
        
        # Add segment to combined audio with crossfade if not the first segment
        if i == 0:
            combined = segment_audio
        else:
            combined = combined.append(segment_audio, crossfade=crossfade_duration)
        
        print(f"Added segment {i+1}: {segment['text'][:50]}...")
    
    # Export combined audio
    combined.export(output_file, format="wav")
    
    # Return total duration
    return len(combined) / 1000  # Convert to seconds

if __name__ == "__main__":
    segments_file = "/home/ubuntu/podcast_project/selected_segments.json"
    output_file = "/home/ubuntu/podcast_project/arranged_highlights.wav"
    
    # Arrange segments
    print("Arranging segments with smooth transitions...")
    total_duration = arrange_segments(segments_file, output_file)
    
    print(f"Arranged highlight reel created with duration: {total_duration:.2f} seconds")
