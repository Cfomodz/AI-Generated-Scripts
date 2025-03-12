import json
from pydub import AudioSegment
import os

def create_transcript_document(segments_file, output_file):
    """
    Create a transcript document with timestamps and quotes
    
    Args:
        segments_file: Path to the selected segments JSON file
        output_file: Path to save the transcript document
    """
    # Load segments info
    with open(segments_file, 'r') as f:
        segments = json.load(f)
    
    # Create transcript content
    content = "# DeepSeek R1 Podcast - Highlight Reel Transcript\n\n"
    content += "This document contains the transcript of the 2-minute highlight reel created from the DeepSeek R1 Podcast.\n\n"
    
    content += "## Selected Quotes\n\n"
    
    for i, segment in enumerate(segments):
        start_time = segment["start_time"]
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"
        
        content += f"**Quote {i+1}** [Timestamp: {timestamp}]\n"
        content += f"*{segment['text']}*\n\n"
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"Transcript document created at: {output_file}")

if __name__ == "__main__":
    segments_file = "/home/ubuntu/podcast_project/selected_segments.json"
    output_file = "/home/ubuntu/podcast_project/highlight_reel_transcript.md"
    
    # Create transcript document
    create_transcript_document(segments_file, output_file)
