from flask import Flask, render_template, request
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text

app = Flask(__name__)

language_codes = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Spanish": "es", "Chinese (Simplified)": "zh-CN",
    "Russian": "ru", "Japanese": "ja", "Korean": "ko", "German": "de", "French": "fr",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Gujarati": "gu", "Punjabi": "pa","marathi":"mr"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", languages=language_codes.keys())

@app.route("/translate", methods=["POST"])
def translate():
    input_lang = request.form.get("input_lang")
    output_lang = request.form.get("output_lang")

    r = sr.Recognizer()
    recognized_text = ""
    translated_text = ""

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        speech_text = r.recognize_google(audio)
        lang_code = language_codes.get(input_lang, "en")
        transliterated = transliterate_text(speech_text, lang_code) if lang_code != 'en' else speech_text
        recognized_text = transliterated
        translated_text = GoogleTranslator(source='auto', target=language_codes[output_lang]).translate(transliterated)

        tts = gTTS(translated_text, lang=language_codes[output_lang])
        tts.save("output.mp3")
        playsound("output.mp3")
        os.remove("output.mp3")

    except:
        recognized_text = "Could not understand audio."
        translated_text = "Translation failed."

    return render_template("index.html",
                           languages=language_codes.keys(),
                           recognized_text=recognized_text,
                           translated_text=translated_text)

if __name__ == "__main__":
    app.run(debug=True)
