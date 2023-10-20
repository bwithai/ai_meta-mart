from typing import Optional

import openai


class Chat:

    def __init__(self, system: Optional[str] = None):
        self.system = system
        self.messages = []

        if system is not None:
            self.messages.append({
                "role": "system",
                "content": system
            })

    def prompt_for_json(self, content: str) -> str:
        self.messages.append({
            "role": "user",
            "content": content
        })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        response_content = response["choices"][0]["message"]["content"]
        self.messages.append({
            "role": "assistant",
            "content": response_content
        })
        return response_content

    def prompt(self, content: str) -> str:
        self.messages.append({
            "role": "user",
            "content": "if user place some order say 'write some soft professional word to say order will be place in your cart' in professional AND friendly way:\n" + content
        })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        response_content = response["choices"][0]["message"]["content"]
        self.messages.append({
            "role": "assistant",
            "content": response_content
        })
        return response_content
