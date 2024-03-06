import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from local_components import card_container 
#from pandasai import SmartDataframe
#from pandasai.llm import OpenAI
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

st.title(":blue[Drop]Table")

#header ke niche
col1, col2 = st.columns(2)
with col1:
	with st.expander("👆 Select your desired tone of output."):
		st.write("Sample")

with col2:
	with st.expander("🔗 Connect your data to a data source."):
		st.write("Sample")
col3, col4 = st.columns(2)
with col3:
	with st.expander("🔍 Ask questions and query out results."):
		st.write("Sample")
with col4:
	with st.expander("👀 Analyse charts and graphs visually."):
		st.write("Sample")

st.sidebar.write("Use DropTables' highly customized and fine-tuned **Generative-AI** features to build data analytics visualization dashboards.")

#Select temperature of GoogleGenAI
tabselect = ui.tabs(options=['Creative', 'Medium', 'Precise'], default_value='Medium', key="temperature")
if tabselect == "Creative":
	temp = 0.8
elif tabselect == "Medium":
	temp = 0.5
elif tabselect == "Precise":
	temp = 0.2
	
#sidebar initial elements
title = st.sidebar.text_input('Enter your use-key', placeholder="Enter your private use-key",key="placeholder", type="password")
buybutton = st.sidebar.link_button("Get your Key", "https://teenscript.substack.com/", type="primary", help="Purchase your private use-key to work with droptable.", use_container_width=True)
st.sidebar.caption('If you dont have a private use-key, then get one and keep it safe.')

#options menu in sidebar
st.sidebar.write("Conversational data analysis 👇")
with st.sidebar:
	selected2 = option_menu(None, ["Enable", "Disable"], 
    icons=['eye', 'eye-slash'], 
    menu_icon=None, default_index=0, orientation="horizontal")
	

tab = ui.tabs(options=['Local file', 'Google sheets', 'Airtable', 'Snowflake'], default_value='Local file', key="select")
if tab == "Local file":

	with card_container():
		uploaded_file = st.file_uploader("Choose a file 📂", type=["csv"])
		#Check is file is uploaded or not
	if uploaded_file is None:
		st.info("Upload a .csv or .xlsx spreadsheet file to continue", icon="ℹ️")
	if uploaded_file is not None:
		# Llama-index Queryt Engine
		df = pd.read_csv(uploaded_file, encoding='latin-1')
		query_engine = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)
		with st.spinner("Generating Summary..."):
			response = query_engine.query("List down point wise all possible types of relationships and correlations that can be driven out of the dataset in detail with explanations and examples.")
			response1 = query_engine.query("Analyse the dataset, and drive valuable insights and write a detailed report, the different visualizations, different insightfu; indicators etc.")
			with card_container():
				st.markdown(response)
			with card_container():
				st.markdown(response1)
		
elif tab == "Google sheets":
	st.write("Google Sheets")

elif tab == "Airtable":
	st.write("Airtable")
		
elif tab == "Snowflake":
	st.write("Snowflake")

