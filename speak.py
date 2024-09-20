import speech_recognition as sr
import pyttsx3
import brain as friday
import csv

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Set the voice to female
# List all available voices
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name:
        engine.setProperty('voice', voice.id)
        print(f"Selected female voice: {voice.name}")
        break
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
def load_data(data_file,contexts):
    print("Data loading...")
    with open(data_file, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        header = header[0].split(',')  # Split the header by commas

        # Get the index of the 'context' column
        context_index = header.index('context')

        # Loop through the remaining rows and collect context data
        for row in csv_reader:
            row = row[0].split(',')  # Split the row by commas
            contexts.append(row[context_index])  # Append the context to the list

    # Concatenate all contexts into a single string
    all_contexts = ' '.join(contexts)

    return all_contexts
def main():
    # Đọc file CSV và đảm bảo pandas đọc đúng header
    data_file = 'question_answer_data.csv'
    contexts = []
    context = load_data(data_file,contexts)
    print(f"Context (all joined): {context}")

    while True:
        query = listen()
        if query:
            if 'stop' in query.lower():
                speak("Goodbye boss!")
                break
            elif 'hello' in query.lower():
                speak("Hello boss, I am Friday. How can I assist you today?")
            else:
                # Xử lý câu hỏi thông thường
                answer = friday.response(query, context)  # Gọi hàm response
                speak(answer)  # Nói câu trả lời

if __name__ == "__main__":
    main()