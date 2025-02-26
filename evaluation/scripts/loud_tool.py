import argparse
from pathlib import Path
import torchaudio

# Function to scan directory and find all audio files
def scan_directory(directory):
    audio_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
    audio_files = [f for f in Path(directory).rglob('*') if f.suffix.lower() in audio_extensions]
    return audio_files

# Function to measure the integrated loudness and duration of an audio file
def measure_loudness(file_path):
    # Load audio file
    waveform, sample_rate = torchaudio.load(file_path)
    
    # Measure loudness of the original waveform (without downmixing)
    loudness = torchaudio.functional.loudness(waveform, sample_rate)
    
    # Calculate duration in seconds
    duration = waveform.size(1) / sample_rate
    
    return loudness, waveform, sample_rate, duration

# Function to modify loudness to target LUFS using fixed gain
def apply_fixed_gain(waveform, gain_db):
    # Apply the gain to the entire waveform (all channels)
    gain_factor = 10 ** (gain_db / 20)
    adjusted_waveform = waveform * gain_factor
    
    # Check for clipping
    if (adjusted_waveform.abs() > 1.0).any():
        print("Warning: Audio clipping detected after applying fixed gain. Normalizing to 1.0 . . .")
        adjusted_waveform = waveform / (waveform.abs().max().item())
    
    return adjusted_waveform

# Function to normalize loudness per file to target LUFS
def normalize_loudness_per_file(waveform, sample_rate, target_loudness):
    # Measure the loudness of the file
    current_loudness = torchaudio.functional.loudness(waveform, sample_rate)
    
    # Calculate gain needed to reach target loudness
    gain_db = target_loudness - current_loudness
    gain_factor = 10 ** (gain_db / 20)
    
    # Apply the gain to the entire waveform (all channels)
    adjusted_waveform = waveform * gain_factor
    
    # Check for clipping
    if (adjusted_waveform.abs() > 1.0).any():
        print("Warning: Audio clipping detected after normalization. Normalizing to 1.0 . . .")
        adjusted_waveform = waveform / (waveform.abs().max().item())
    
    return adjusted_waveform

# Function to calculate summary statistics
def calculate_statistics(loudness_values):
    mean_loudness = sum(loudness_values) / len(loudness_values)
    max_loudness = max(loudness_values)
    min_loudness = min(loudness_values)
    return mean_loudness, max_loudness, min_loudness

# Main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Measure and optionally adjust integrated loudness of audio files in a directory.")
    parser.add_argument('directory', type=str, help="Directory to scan for audio files")
    parser.add_argument('--per-file', action='store_true', help="Print loudness for each file")
    parser.add_argument('--target-lufs', type=float, help="Target LUFS to adjust the loudness of all files")
    parser.add_argument('--mode', choices=['fixed-gain', 'loudness-norm', 'peak-norm'], default='loudness-norm', 
                        help="Mode for adjusting loudness: 'fixed-gain' applies the same gain to all files, 'loudness-norm' normalizes each file to the target LUFS, 'peak-norm' normalizes to maximum peak")
    
    args = parser.parse_args()
    directory = args.directory
    target_lufs = args.target_lufs
    mode = args.mode
    # Scan for audio files
    audio_files = scan_directory(directory)
    
    if not audio_files:
        print("No audio files found.")
        return
    
    loudness_values = []
    peak_values = []
    total_duration = 0  # Total duration of all files

    # Measure loudness, peak, and duration of each file
    for file_path in audio_files:
        try:
            loudness, waveform, sample_rate, duration = measure_loudness(file_path)
            loudness_values.append(loudness)
            
            # Compute peak value
            peak_value = waveform.abs().max().item()
            peak_values.append(peak_value)
            
            total_duration += duration
            
            # Optionally print per-file loudness
            if args.per_file:
                print(f"File: {file_path} | Integrated Loudness: {loudness:.2f} LUFS | Duration: {duration:.2f} seconds")
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    if target_lufs is not None:
        if not loudness_values:
            print("No loudness values available to adjust.")
            return
        
        # Calculate average loudness
        average_loudness = sum(loudness_values) / len(loudness_values)
        
        if mode == 'fixed-gain':
            # Calculate gain needed to adjust the average loudness to the target LUFS
            gain_db = target_lufs - average_loudness
            
            # Apply the gain to all files
            for file_path in audio_files:
                try:
                    # Re-load the file
                    waveform, sample_rate = torchaudio.load(file_path)
                    
                    # Apply fixed gain
                    adjusted_waveform = apply_fixed_gain(waveform, gain_db)
                    
                    # Save adjusted file (overwrite original for simplicity)
                    torchaudio.save(file_path, adjusted_waveform, sample_rate)
                    print(f"File: {file_path} adjusted to target LUFS using fixed gain")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        elif mode == 'loudness-norm':
            # Apply loudness normalization per file
            for file_path in audio_files:
                try:
                    # Re-load the file
                    waveform, sample_rate = torchaudio.load(file_path)
                    
                    # Normalize loudness
                    adjusted_waveform = normalize_loudness_per_file(waveform, sample_rate, target_lufs)
                    
                    # Save adjusted file (overwrite original for simplicity)
                    torchaudio.save(file_path, adjusted_waveform, sample_rate)
                    print(f"File: {file_path} normalized to target LUFS")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
    elif mode == 'peak-norm':
        if not peak_values:
            print("No peak values available to adjust.")
            return
        
        # Calculate the maximum peak
        max_peak = max(peak_values)
        print(peak_values,max_peak)
        # Calculate the gain needed to normalize the maximum peak to 1.0
        peak_gain = 1.0 / max_peak
        
        # Apply the peak normalization to all files
        for file_path in audio_files:
            try:
                # Re-load the file
                waveform, sample_rate = torchaudio.load(file_path)
                
                # Apply peak normalization
                adjusted_waveform = waveform *  peak_gain
                
                # Save adjusted file (overwrite original for simplicity)
                torchaudio.save(file_path, adjusted_waveform, sample_rate)
                print(f"File: {file_path} normalized with gain {peak_gain:.2f}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Recalculate loudness values after adjustment
    loudness_values = []
    peak_values = []
    for file_path in audio_files:
        try:
            loudness, waveform, _, _ = measure_loudness(file_path)
            loudness_values.append(loudness)
            peak_value = waveform.abs().max().item()
            peak_values.append(peak_value)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Calculate and print summary statistics
    if loudness_values:
        mean_loudness, max_loudness, min_loudness = calculate_statistics(loudness_values)
        
        print(f"\nSummary Statistics:")
        print(f"Mean Integrated Loudness: {mean_loudness:.2f} LUFS")
        print(f"Maximum Integrated Loudness: {max_loudness:.2f} LUFS")
        print(f"Minimum Integrated Loudness: {min_loudness:.2f} LUFS")
        print(f"Total Duration: {total_duration:.2f} seconds")
        print(f"Max Peak Value: {max(peak_values):.2f}")

if __name__ == '__main__':
    main()
