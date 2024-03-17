from openai import OpenAI
import os
import re
import ast

#**************************************************************************************************#
#* GPT Query                               														  *#
#**************************************************************************************************#


def query_gpt(model_description):

    # Ensure this environment variable is set in your OS
    # key = os.getenv('OPENAI_API_KEY')

    # if key is None:
    #     raise Exception("The OPENAI_API_KEY environment variable is not set.")

    #-----------------------------GPT START
    #Now 'model_description' variable contains the text from the file
    #print(model_description)
        
    client = OpenAI(api_key= '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')

    completion = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
        {
            "role": "system",
            "content": "Assistant is a large language model trained by OpenAI."
        },
        {"role": "user", "content": model_description}
    ],
    temperature=0.15,  # Low temperature to reduce randomness
    #   top_p=1,  # Use the full range of the model's capabilities
    #   frequency_penalty=0,  # No frequency penalty
    #   presence_penalty=0  # No presence penalty
    )

    # Extract the message from the response
    m = completion.choices[0].message.content #MUST BE CONTENT

    message = str(m) #NEED EXPLICIT TYPE CAST
    print(message)
    return message

    #----------------------END GPT
