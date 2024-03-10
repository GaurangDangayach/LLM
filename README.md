# Google Sheet Query Engine
This app is built using LangChain, QDrant Cloud and Streamlit. It can be used to get answers to question based on the responses (regietration details) from a Google Sheet built by Google Forms. Using LLM we can add addtional features like granted limited access to eployees to the personal data of the registered people.

To use the app do the following -

**Pre-Requisites:**
* Hugging Face API token (can be created after creating Hugging Face account)
* QDrant Cloud API Key (can be created after creating QDrant cloud account)
* Stramlit Account

1. Clone the repository.
2. In the _sheets_app.py_ file, add your Hugging Face API token and QDrant Cloud API key in the respective spaces.
3. Deploy the app on Streamlit Cloud server.
4. In the text box, add the editable (public access) link of the Response Sheet.
5. Type your question and click on Submit to get the answer.

_**Note:** I am currently facing a bug in the code in using Google Sheets API because of which the code is not running._
