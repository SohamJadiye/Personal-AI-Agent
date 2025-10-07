import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Listening (say something)...")
        try:
            # Listen with a maximum of 5 seconds for silence
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected for a while. Stopping...")
            break

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        if "exit" in text.lower():
            print("Exiting...")
            break
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Request failed; {e}")
