import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from local_components import card_container 
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from llama_index.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context


st.set_page_config(
    page_title="DropTable",
    page_icon="🐻"
)

llm = OpenAI(api_token=st.secrets["OpenAI_Key"])

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
		queryengine = PandasQueryEngine(df=df, instruction_str=instruction_str)
		queryengine.update_prompts({"pandas_prompt": new_prompt})
		user = st.text_input('Ask question...')
		if user:
			with st.spinner("Generating Summary..."):
				ans = queryengine.query(user)
				with card_container():
					st.write(ans)
		
elif tab == "Google sheets":
	st.write("Chat")
elif tab == "Airtable":
	st.write("Vision")
elif tab == "Manual":
	st.write("Snowflake")

