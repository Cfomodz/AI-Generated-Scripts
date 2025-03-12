import json
from pydub import AudioSegment
import os

def validate_highlight_reel(audio_file, segments_file):
    """
    Validate the quality of the highlight reel
    
    Args:
        audio_file: Path to the highlight reel audio file
        segments_file: Path to the selected segments JSON file
    
    Returns:
        Validation results
    """
    # Load the highlight reel
    audio = AudioSegment.from_wav(audio_file)
    
    # Load segments info
    with open(segments_file, 'r') as f:
        segments = json.load(f)
    
    # Check duration
    duration = len(audio) / 1000  # Convert to seconds
    duration_check = duration <= 120
    
    # Check number of segments
    segment_count = len(segments)
    
    # Prepare validation results
    results = {
        "file_path": audio_file,
        "duration": f"{duration:.2f} seconds",
        "duration_check": "PASS" if duration_check else "FAIL",
        "segment_count": segment_count,
        "segments": [segment["text"][:50] + "..." for segment in segments],
        "overall_quality": "PASS" if duration_check else "FAIL"
    }
    
    return results

if __name__ == "__main__":
    audio_file = "/home/ubuntu/podcast_project/DeepSeek-R1-Podcast-Highlights.wav"
    segments_file = "/home/ubuntu/podcast_project/selected_segments.json"
    
    # Validate highlight reel
    print("Validating highlight reel quality...")
    results = validate_highlight_reel(audio_file, segments_file)
    
    # Print validation results
    print("\nValidation Results:")
    print(f"File: {results['file_path']}")
    print(f"Duration: {results['duration']} (Target: ≤ 120 seconds) - {results['duration_check']}")
    print(f"Number of segments: {results['segment_count']}")
    print("\nSegments included:")
    for i, segment in enumerate(results['segments']):
        print(f"{i+1}. {segment}")
    
    print(f"\nOverall Quality: {results['overall_quality']}")
    
    # Save validation results
    with open("/home/ubuntu/podcast_project/validation_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nValidation results saved to: /home/ubuntu/podcast_project/validation_results.json")
