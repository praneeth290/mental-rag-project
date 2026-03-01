import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    files = ["video1.mp3", "video2.mp3"]

    full_text = ""

    for file in files:
        print(f"Transcribing {file}...")
        text = transcribe_audio(file)
        full_text += text + "\n\n"

    with open("mdd_transcript.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("Transcript created successfully.")