from flask import Flask, request, render_template
from pydub import AudioSegment
import speech_recognition as sr
import io
import wolframalpha

app = Flask(__name__)

APP_ID = "EP4H5KV6H9"
client = wolframalpha.Client(APP_ID)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recognize', methods=['POST'])
def recognize_audio():
    if 'audio_data' not in request.files:
        return "No audio file uploaded", 400

    file = request.files['audio_data']
    audio_bytes = io.BytesIO(file.read())

    try:
        # Convert webm to wav
        audio_segment = AudioSegment.from_file(audio_bytes, format="webm")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print("Recognized Text:", text)

        try:
            res = client.query(text)
            answer = next(res.results).text
            print("Wolfram|Alpha Answer:", answer)

        except StopIteration:
            print("No result found")
            return "No result found", 404

        except Exception as wolfram_error:
            print("Wolfram|Alpha Error:", str(wolfram_error))
            return f"Wolfram|Alpha Error: {str(wolfram_error)}", 500

    except Exception as e:
        print("General Error:", str(e))
        return f"Error: {str(e)}", 500
    
    return answer


if __name__ == "__main__":
    app.run(debug=True)
