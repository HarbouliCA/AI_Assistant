import openai
import pyttsx3
import speech_recognition as sr
import time
import os
import speech_recognition as sr

#If you using windows, you might need to install PyAudio to increase the voice recongnition process

#API KEY FROM WEBSITE
openai.api_key = "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"

#Initalize the text from speech engine:
engine = pyttsx3.init()

#Transcript audio to text function
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Unknown Error')

#Generate responses from ChatGPT
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002", # calling GPT3 model
        prompt=prompt,
        max_tokens=2024, #maximum toxen is 4096 for GPT3
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

#speak Function
def speak_text(text):
    engine.say(text)
    engine.runAndWait()


#Constructing the Logic

def main():
    while True:
        #wait for user to say "ghost"
        print("Say GHOST to start recording your question ...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == 'ghost':
                #record Audio
                    filename = "input.wav"
                    print('Say you question')
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    #Transcibe the audio to text:
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate the response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read the response using Text to seech
                        speak_text(response)

            except Exception as e:
                print("An error occurred : {}".format(e))

if __name__ == "__main__":
    main()
