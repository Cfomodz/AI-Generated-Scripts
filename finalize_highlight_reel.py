import json
from pydub import AudioSegment
import os

def finalize_highlight_reel(input_file, output_file, target_duration=120):
    """
    Finalize the highlight reel by adding fade in/out effects
    
    Args:
        input_file: Path to the arranged audio file
        output_file: Path to save the final highlight reel
        target_duration: Target duration in seconds
    
    Returns:
        Final duration of the highlight reel
    """
    # Load the arranged audio
    audio = AudioSegment.from_wav(input_file)
    
    # Add fade in and fade out effects
    fade_in_duration = 1000  # 1 second
    fade_out_duration = 1500  # 1.5 seconds
    
    audio = audio.fade_in(fade_in_duration).fade_out(fade_out_duration)
    
    # Check if duration is within target
    current_duration = len(audio) / 1000  # Convert to seconds
    print(f"Current duration: {current_duration:.2f} seconds")
    
    if current_duration > target_duration:
        # Trim if needed to meet target duration
        audio = audio[:target_duration * 1000]
        print(f"Trimmed to {target_duration} seconds")
    
    # Export final audio
    audio.export(output_file, format="wav")
    
    # Return final duration
    return len(audio) / 1000  # Convert to seconds

if __name__ == "__main__":
    input_file = "/home/ubuntu/podcast_project/arranged_highlights.wav"
    output_file = "/home/ubuntu/podcast_project/DeepSeek-R1-Podcast-Highlights.wav"
    
    # Finalize highlight reel
    print("Finalizing highlight reel...")
    final_duration = finalize_highlight_reel(input_file, output_file)
    
    print(f"Final highlight reel created with duration: {final_duration:.2f} seconds")
    print(f"Saved to: {output_file}")
