from kani import Kani, chat_in_terminal
from kani.engines.openai import OpenAIEngine
import gradio as gr
#api_key = "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"
import openai
import asyncio
from kani import ChatMessage
from dotenv import load_dotenv
import os 

load_dotenv()
my_key = os.getenv("OPENAI_API_KEY")
engine = OpenAIEngine(my_key, model="gpt-3.5-turbo")

async def cpAssistantModel(transcript):
    fewshot = [
        ChatMessage.system("You are helping the caregiver of a cerebral palsy patient understand what the cerebral palsy patient is trying to say. You will typically receive under 3 words and will have to form entire sentences in the first person conveying what the input actually means. Remember, the input might be misspelled or the letters might be in the wrong order. ALWAYS respond in FIRST PERSON"),

        ChatMessage.user("walk"),

        ChatMessage.assistant("I need help walking to the door"),

        ChatMessage.user("bath"),

        ChatMessage.assistant("I need help taking a bath"),

        ChatMessage.user("drink"),

        ChatMessage.assistant("I want something to drink"),
    ]

    ai = Kani(engine, chat_history=fewshot)
    counter = 0
    while True:
        user_input = ""
        if counter != 0:
            user_input = input("Your input: ")
            counter +=1
        if user_input.lower() == "quit":
            break
        if counter == 0:
            user_input = transcript
            counter +=1    
        
        
        response = await ai.chat_round_str(user_input)
        print("AI:", response)

def process_audio(file_path):
    audio = open(file_path, "rb")
    openai.api_key = my_key
    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio, response_format='text')
    return transcript

def main():
    user_choice = input("Enter '1' to provide transcript via chat terminal or '2' to provide an audio file: ")

    if user_choice == '1':
        transcript = input("Enter the transcript: ")
        asyncio.run(cpAssistantModel(transcript))

    elif user_choice == '2':
        audio_file_path = "cpAudio.mp3"
        transcript = process_audio(audio_file_path)
        asyncio.run(cpAssistantModel(transcript))
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()