import cv2
import pyaudio
import wave
import threading
import subprocess
import time
import os

# --- AUDIO CONFIGURATION ---
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100
AUDIO_CHUNK = 1024


class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(format=AUDIO_FORMAT, channels=AUDIO_CHANNELS,
                                      rate=AUDIO_RATE, input=True, frames_per_buffer=AUDIO_CHUNK)
        # Start recording in a background thread
        threading.Thread(target=self._record).start()

    def _record(self):
        while self.is_recording:
            data = self.stream.read(AUDIO_CHUNK)
            self.frames.append(data)

    def stop(self, filename="temp_audio.wav"):
        self.is_recording = False
        time.sleep(0.1)  # Let the thread finish
        self.stream.stop_stream()
        self.stream.close()

        # Save to WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(AUDIO_RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()


def merge_audio_video(video_path, audio_path, output_path):
    """Uses FFmpeg to combine the silent video and the audio file."""
    print("🎬 Merging Audio and Video...")
    cmd = f"ffmpeg -y -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}"
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Cleanup temporary files
    os.remove(video_path)
    os.remove(audio_path)
    print(f"✅ Saved final video with sound: {output_path}")


# --- MAIN LOOP LOGIC ---

audio_recorder = AudioRecorder()
is_recording_event = False
video_writer = None

# ... [Your OpenCV Setup] ...

while cap.isOpened():
    ret, frame = cap.read()

    # ... [Your motion detection logic: if changed_pixels > Threshold] ...
    motion_detected = changed_pixels > 5000

    if motion_detected:
        last_motion_time = time.time()

        # If we weren't already recording, start both Video AND Audio!
        if not is_recording_event:
            print("🔴 Motion started! Recording Video and Audio...")
            is_recording_event = True
            video_writer = cv2.VideoWriter('temp_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))
            audio_recorder.start()

    # If we are currently in a recording event...
    if is_recording_event:
        video_writer.write(frame)

        # Check if the cooldown period has expired (e.g., 5 seconds of no motion)
        if time.time() - last_motion_time > 5:
            print("⏹️ Motion stopped. Finishing recording...")
            is_recording_event = False

            # Stop Video
            video_writer.release()
            # Stop Audio
            audio_recorder.stop("temp_audio.wav")

            # Merge them together!
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            merge_audio_video("temp_video.avi", "temp_audio.wav", f"Event_{timestamp}.mp4")


