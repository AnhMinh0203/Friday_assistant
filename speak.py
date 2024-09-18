import speech_recognition as sr
import pyttsx3
import pandas as pd
from transformers import pipeline
import main as friday

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='en-US')
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return ""


def answer_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']


def main():
    # Load the CSV file containing context, questions, answers
    # data = pd.read_csv('question_answer_data.csv')

    # Loop through the CSV and use the context for answering
    # contexts = data['context'].tolist()

    speak("Hello, I am Friday. How can I assist you today?")

    context_index = 0  # To track which context we are using
    while True:
        query = listen()
        if query:
            if 'stop' in query.lower():
                speak("Goodbye!")
                break
            # elif 'start' in query.lower():
            #     context = contexts[context_index % len(contexts)]  # Get current context
            #     friday.response(query.lower(), context)  # Pass context to friday.response()
            #     context_index += 1  # Move to the next context in the next loop
            else:
                # Use the current context to answer the question
                # context = contexts[context_index % len(contexts)]
                # answer = answer_question(query, context)
                speak(f"The answer is")


if __name__ == "__main__":
    main()