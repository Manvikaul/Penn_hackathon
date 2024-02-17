from kani import Kani, chat_in_terminal
from kani.engines.openai import OpenAIEngine
api_key = "sk-"
engine = OpenAIEngine(api_key, model="gpt-3.5-turbo")
from kani import ChatMessage

fewshot = [
    ChatMessage.system("Your are helping the caregiver of a cerebral palsy patient understand what the cerebral palsy patient is trying to say. You will typically receive under 3 words and will have to form entire sentences in first person conveying what the input actually means. Remember, the input might be mispelt or the letters might be in the wrong order."),

    ChatMessage.user("walk"),

    ChatMessage.assistant("I need help walking to the door"),

    ChatMessage.user("bath"),

    ChatMessage.assistant("I need help taking a bath"),
    
    ChatMessage.user("drink"),

    ChatMessage.assistant("I want something to drink"),

]
ai = Kani(engine, chat_history=fewshot)
chat_in_terminal(ai)