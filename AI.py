from openai import AzureOpenAI
import streamlit as st

class Talker:
    def __init__(self, api_key = st.secrets['api']['api_key'], api_version="2023-05-15", azure_endpoint="https://hkust.azure-api.net"):
        """
        Initialize the Talker with Azure OpenAI credentials.
        """
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        
    def get_response(self, query: str, instruction: str) -> str:
        """
        Generate a semantic search response using Azure OpenAI.
        :param query: User's input query.
        :param instruction: Additional instructions for GPT to enhance the query.
        :return: The response generated by GPT.
        """
        response = self.client.chat.completions.create(
            model="gpt-35-turbo",
            temperature=0.5,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content