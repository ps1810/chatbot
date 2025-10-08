from typing import List

class Message:

    def __init__(self, content:str, role:str):
        self.content = content
        self.role = role


class Conversation:

    def __init__(self, messages: List[Message]):
        self.messages = messages