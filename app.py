
import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from local_components import card_container 
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
import openai
from IPython.display import Markdown, display
from streamlit_option_menu import option_menu
#from prompts import new_prompt, instruction_str, context



st.set_page_config(
    page_title="DropTable",
    page_icon="🐻",
    initial_sidebar_state="expanded",
)

llm = OpenAI(api_token=st.secrets["OpenAI_Key"])
openai.api_key = st.secrets["OpenAI_Key"]

instruction = """\
1.Convert the dataset and summarize with every important points.
2.Give all detailes to be fed to Google Gemini for summarization and analysis.

"""

st.title(":blue[Drop]Table")

st.sidebar.write("Use DropTables' highly customized and fine-tuned **Generative-AI** features to build data analytics visualization dashboards.")

	
#sidebar initial elements
title = st.sidebar.text_input('Enter your use-key', placeholder="Enter your private use-key",key="placeholder", type="password")
buybutton = st.sidebar.link_button("Get your Key", "https://teenscript.substack.com/", type="primary", help="Purchase your private use-key to work with droptable.", use_container_width=True)
st.sidebar.caption('If you dont have a private use-key, then get one and keep it safe.')
	

# Data source selection
tab = ui.tabs(options=['Local file', 'Google sheets', 'Airtable', 'Snowflake'], default_value='Local file', key="select")
if tab == "Local file":
    uploaded_file = st.sidebar.file_uploader("Choose a file 📂", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='latin-1')
        querydata = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)
	    
if tab == "google sheets":
	st.write("Google Sheets")

if tab == "Airtable":
	st.write("Airtable")
		
if tab == "Snowflake":
	st.write("Snowflake")




