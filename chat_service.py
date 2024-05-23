from typing import TypedDict

import ollama

class OllamaMessage(TypedDict):
  role: str
  content: str

  
type OllamaMessages = list[OllamaMessage]

  
def query(prompt: str, chat_history: OllamaMessages) -> tuple[OllamaMessage, OllamaMessages]:

  newMessage: OllamaMessage = {'role': 'user', 'content': prompt}

  chat_history.append(newMessage)

  stream = ollama.chat(
      model='phi3',
      messages=chat_history,
      stream=True,
  )

  responseContent: str = ""
  for chunk in stream:
      message: str = chunk['message']['content'] or ""
      responseContent += message
      print(message, end='', flush=True)

  response: OllamaMessage = {'content': responseContent, 'role': 'system'}

  chat_history.append(response)

  return (response, chat_history)



