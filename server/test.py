import pyttsx3
engine = pyttsx3.init()

engine.setProperty('rate', 170)   
engine.setProperty('volume', 1.0)  


text = "Hello Soham, the answer is 8."
engine.say(text)

# Block while speaking
engine.runAndWait()