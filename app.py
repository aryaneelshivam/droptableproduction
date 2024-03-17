
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

# Data source selection
tab = ui.tabs(options=['Local file', 'Google sheets', 'Airtable', 'Snowflake'], default_value='Local file', key="select")

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

	
#sidebar initial elements
title = st.sidebar.text_input('Enter your use-key', placeholder="Enter your private use-key",key="placeholder", type="password")
buybutton = st.sidebar.link_button("Get your Key", "https://teenscript.substack.com/", type="primary", help="Purchase your private use-key to work with droptable.", use_container_width=True)
st.sidebar.caption('If you dont have a private use-key, then get one and keep it safe.')
	

# Columns for two sections
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
    user_input = st.text_area("Enter your input 💬", placeholder="Enter your question/query")  
    enter_button = st.button("Enter ⚡", use_container_width=True, type="primary")

with col4:
    with st.expander("👀 Analyse charts and graphs visually."):
        st.write("Sample")
    output = st.text_area("Your generated output 🎉", placeholder="The output will be displayed here")
    generate = st.button("Generate AI report ⚡", use_container_width=True)

st.write(" ")
#tab1, tab2 = st.tabs(["Generate AI report 🔄", "Manual plotting 🖐"])




if tab == "Local file":
	uploaded_file = st.sidebar.file_uploader("Choose a file 📂", type=["csv"])
	#Check is file is uploaded or not
	if uploaded_file is None:
		st.info("Upload a .csv or .xlsx spreadsheet file to continue", icon="ℹ️")
	if uploaded_file is not None:
		# Llama-index Queryt Engine
		df = pd.read_csv(uploaded_file, encoding='latin-1')
		#llm = OpenAI(api_token=st.secrets["OpenAI_Key"])
		#sdf = SmartDataframe(df, config={"llm": llm})
		st.dataframe(df)
		query_engine = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)
		tab1, tab2, tab3 = st.tabs(["AI report 📌", "Generative chat 💬", "DropAI vision 👁‍🗨"])
		with tab1:
			generate = st.button("Generate AI analysis ⚡",use_container_width=True)
			manual = st.toggle("Enable manual plotting")
			#if user hits generate button
			if generate:
				st.session_state.generate_state = True
				with st.spinner("Exploring data..."):
					response = query_engine.query("List down point wise all possible types of relationships and correlations that can be driven out of the dataset in detail with explanations and examples.")
				if response:
					with st.spinner("Analysing data..."):
						response2 = query_engine.query("Summarize the entire dataset")
				if response2:
					with st.spinner("Generating summary..."):
						response1 = query_engine.query("Analyse the dataset, and drive valuable insights and write a detailed report, the different visualizations, different insightfu; indicators etc.")
				if response1:
					with st.spinner("Generating visualizations..."):
						plot = query_engine.query("Generate Python executable code to plot multiple chart types like, bar chart, pie chart, line chart, histogram and scatter plot. Ensure the code is structured to plot different types of charts. Use subplots. Code only.")
					with card_container():
						st.markdown(response2)
					with card_container():
						st.markdown(response1)
					with card_container():
						st.markdown(response)
					with st.spinner("Generating plots..."):
						code = st.code(plot, language='python')
						st.echo(code)
						exec(str(plot))
						st.set_option('deprecation.showPyplotGlobalUse', False)
						st.pyplot(use_container_width=True)
		with tab2:
			#Conversational Ai part:
			if selected2 == "Enable":
				convfile = st.sidebar.file_uploader("Choose a file to talk 💬", type=["csv"], key="conv")
				if convfile is not None:
					data = pd.read_csv(convfile, encoding='latin-1')
					with st.container():
						querydata = PandasQueryEngine(df=data, verbose=True, synthesize_response=True)
						txt = st.text_area("Enter your query 💬")
						if txt:
							with st.spinner("Generating answer..."):
								conv = querydata.query(txt)
								st.info(conv, icon="💡")
				if convfile is None:
					st.warning("Connect to a source to get conversational capabilities.")
			elif selected2 == "Disable":
				st.error("The conversational feature is disabled, please select 'enable' to enable.", icon="🚨")
		with tab3:
			st.warning("DropAI vision is currently not available in the Beta Version.", icon="⚠")

					
		
if tab == "google sheets":
	st.write("Google Sheets")

if tab == "Airtable":
	st.write("Airtable")
		
if tab == "Snowflake":
	st.write("Snowflake")

