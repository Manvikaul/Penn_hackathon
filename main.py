from kani import Kani, chat_in_terminal
from kani.engines.openai import OpenAIEngine
import gradio as gr
import openai
import asyncio
from kani import ChatMessage
from dotenv import load_dotenv
import os 

load_dotenv()
my_key = os.getenv("OPENAI_API_KEY")
engine = OpenAIEngine(my_key, model="gpt-4")

async def cpAssistantModel(transcript):
    fewshot = [
        ChatMessage.system("You are helping the caregiver of a cerebral palsy patient understand \
            what the cerebral palsy patient is trying to say. You will typically receive under 3 words, \
            and the input maybe misspelt or incomplete; it might also be badly transcribed from audio.\
            Based on that input, you will try to understand the user's intention and confirm that with \
            the user by asking. If the user says no or 'n', that means your original suggestion is wrong, and \
            you will make another suggestion; keep doing this until the user says yes or 'y'. \
            If the user says yes or 'y', check if this intent is specific enough for the caregiver to take action; if not, keep following up \
            in the form more specific suggestions, and confirming with the user in the way as mentioned earlier. \
            At the end, rephrase the user's more specific intent in first-person as the message the user wants to tell the caregiver. \
            If you have trouble understanding the user's intent, try to ask them if the words you received is \
            what they are trying to say, e.g. 'Are you trying to say walk?'; if not, make guesses with words with \
            similar pronunciations."),

        ChatMessage.user("walk"),
        ChatMessage.assistant("Do you need help walking to the door?"),
        ChatMessage.user("n"),
        ChatMessage.assistant("Do you want to go out for a walk?"),
        ChatMessage.user("y"),
        ChatMessage.assistant("Would you like to go out for a walk in the park?"),
        ChatMessage.user("n"),
        ChatMessage.assistant("Would you like to go out for a walk to the supermarket?"),
        ChatMessage.user("yes"),
        ChatMessage.assistant("I want to go out for a walk to the supermarket."),

        ChatMessage.user("bath"),
        ChatMessage.assistant("Do you need help taking a bath?"),
        ChatMessage.user("yeah"),
        ChatMessage.assistant("I need help taking a bath"),

        ChatMessage.user("drin"),
        ChatMessage.assistant("Do you want something to drink?"),
        ChatMessage.user("y"),
        ChatMessage.assistant("Would you like to drink some water?"),
        ChatMessage.user("n"),
        ChatMessage.assistant("Would you like to drink some orange juice?"),
        ChatMessage.user("n"),
        ChatMessage.assistant("Would you like to drink some milk?"),
        ChatMessage.user("ye"),
        ChatMessage.assistant("I want to drink some milk."),
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
        audio_file_path = input("audio file: ")
        transcript = process_audio(audio_file_path)
        print("transcript: ", transcript)
        asyncio.run(cpAssistantModel(transcript))
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()