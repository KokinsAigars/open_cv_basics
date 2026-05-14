import cv2
import pyaudio
import wave
import threading
import subprocess
import time
import os

p = pyaudio.PyAudio()
print("--- Available Audio Inputs ---")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxInputChannels'] > 0:
        print(f"Index {i}: {dev['name']}")
p.terminate()


    # --- Available Audio Inputs ---
    ### Index 0: Microsoft Sound Mapper - Input
    ### Index 1: Microphone (Webcam C170)
    # Index 5: Primary Sound Capture Driver
    ### Index 6: Microphone (Webcam C170)
    ### Index 12: Microphone (Webcam C170)
    ### Index 16: Microphone (Realtek HD Audio Mic input)
    ### Index 18: Line In (Realtek HD Audio Line input)
    ### Index 19: Stereo Mix (Realtek HD Audio Stereo input)
    ### Index 22: Headset (@System32\drivers\bthhfenum.sys,#2;%1 Hands-Free AG Audio%0;(BT SPEAKER))
    ### Index 23: Microphone (Webcam C170)
    ### Index 26: Headset (@System32\drivers\bthhfenum.sys,#2;%1 Hands-Free AG Audio%0;(JBL LIVE660NC))





print(f"📍 Files are being saved to: {os.getcwd()}")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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

    def start(self, device_index=6): # Let's try Index 1 first
        self.is_recording = True
        self.frames = []
        # Many Logitech cams prefer 48000Hz on Windows
        RATE = 48000
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024
            )
            threading.Thread(target=self._record, daemon=True).start()
            print(f"🎤 Mic Active (Index {device_index} @ {RATE}Hz)")
        except Exception as e:
            print(f"❌ Mic Failed to Open: {e}")
            self.is_recording = False

    def _record(self):
        while self.is_recording:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                if data:
                    self.frames.append(data)
            except:
                break

    def stop(self, filename="temp_audio.wav"):
        self.is_recording = False
        time.sleep(0.3)
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # THE FIX: Don't try to write if the bucket is empty
        if len(self.frames) == 0:
            print("empty audio buffer - nothing to save.")
            return False

        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(48000)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            return True
        except Exception as e:
            print(f"❌ Wave write error: {e}")
            return False


def merge_audio_video(video_path, audio_path, custom_name=None):
    if custom_name:
        output_name = f"{custom_name}.mp4"
    else:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_name = f"Capture_{timestamp}.mp4"

    print(f"🎬 Merging into: {output_name}")

    # Using double quotes for Windows path safety
    cmd = f'ffmpeg -y -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_name}"'
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Cleanup
    if os.path.exists(video_path): os.remove(video_path)
    if os.path.exists(audio_path): os.remove(audio_path)
    print(f"✅ Final video saved!")


# --- INITIALIZATION ---
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

audio_recorder = AudioRecorder()
video_writer = None
is_recording_event = False
last_motion_time = 0

# Baseline for motion
ret, frame = cap.read()
prev_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

print("Starting... Press 'q' to stop.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Motion Logic
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        frame_diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

        motion_detected = cv2.countNonZero(thresh) > 5000

        if motion_detected:
            last_motion_time = time.time()
            if not is_recording_event:
                print("🔴 Recording Started...")
                is_recording_event = True
                video_path = os.path.join(PROJECT_ROOT, 'temp_video.avi')
                video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))
                audio_recorder.start()

        if is_recording_event:
            video_writer.write(frame)

            # Stop if no motion for 3 seconds
            if time.time() - last_motion_time > 3:
                print("⏹️ Recording Stopped.")
                is_recording_event = False
                video_writer.release()
                # Only merge if audio was actually recorded
                has_audio = audio_recorder.stop("temp_audio.wav")

                if has_audio:
                    merge_audio_video("temp_video.avi", "temp_audio.wav")
                else:
                    # If no audio, just rename the silent video to a final name
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    os.rename("temp_video.avi", f"Event_{timestamp}_SILENT.avi")

        cv2.imshow('Motion Camera', frame)
        prev_gray = gray

        if cv2.waitKey(20) & 0xFF == ord('q'):
            print("Keyboard Quit detected.")
            break

finally:
    if is_recording_event:
        print("Finalizing last recording before exit...")
        video_writer.release()
        audio_recorder.stop("temp_audio.wav")
        merge_audio_video("temp_video.avi", "temp_audio.wav")

    cap.release()
    cv2.destroyAllWindows()

