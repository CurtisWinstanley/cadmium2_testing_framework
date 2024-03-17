from openai import OpenAI
import os
import re
import base64
import requests

#**************************************************************************************************#
#* GPT Query                               														  *#
#**************************************************************************************************#


# Ensure this environment variable is set in your OS
# key = os.getenv('OPENAI_API_KEY')

# if key is None:
#     raise Exception("The OPENAI_API_KEY environment variable is not set.")

# with open('gpt4.txt', 'r') as file:
#     model_description = file.read()
# #-----------------------------GPT START
# #Now 'model_description' variable contains the text from the file
# #print(model_description)
    
# client = OpenAI(api_key= '')

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "user", "content": model_description}
#   ],
#   temperature=0.1,  # Low temperature to reduce randomness
#   top_p=1,  # Use the full range of the model's capabilities
#   frequency_penalty=0,  # No frequency penalty
#   presence_penalty=0  # No presence penalty
# )

# # Extract the message from the response
# m = completion.choices[0].message.content #MUST BE CONTENT

# message = str(m) #NEED EXPLICIT TYPE CAST
# print(message)

with open('mission_initialization-5-image.txt', 'r') as file:
    model_question = file.read()

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


api_key = "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"


# Path to your image
image_path = "Mission_Init.jpg"
 
# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f"{model_question}"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ]
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())