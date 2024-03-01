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
#from prompts import new_prompt, instruction_str, context



st.set_page_config(
    page_title="DropTable",
    page_icon="🐻"
)

llm = OpenAI(api_token=st.secrets["OpenAI_Key"])
openai.api_key = st.secrets["OpenAI_Key"]

st.title(":blue[Drop]Table")
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
		query_engine = PandasQueryEngine(df=df, verbose=False, synthesize_response=False, instruction_str="""\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression.""" )
		user = st.text_input('Ask question...')
		if user:
			with st.spinner("Generating Summary..."):
				response = query_engine.query(user)
				with card_container():
					st.write(response)
		
elif tab == "Google sheets":
	st.write("Chat")
elif tab == "Airtable":
	st.write("Vision")
elif tab == "Manual":
	st.write("Snowflake")

