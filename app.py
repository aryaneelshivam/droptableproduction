import streamlit as st
import streamlit_shadcn_ui as ui
from local_components import card_container 


st.set_page_config(
    page_title="DropTable",
    page_icon="💧"
)

st.title(":blue[Drop]Table")
tab = ui.tabs(options=['Local file', 'Google sheets', 'Airtable', 'Snowflake'], default_value='Local file', key="select")
if tab == "Local file":

	with card_container():
		uploaded_file = st.file_uploader("Choose a file 📂", type=["csv","XLSX"])

	#Check is file is uploaded or not
	if uploaded_file is None:
		st.info("Upload a .csv or .xlsx spreadsheet file to continue", icon="ℹ️")
	if uploaded_file is not None:
		st.write("Not Null")

elif tab == "Google sheets":
	st.write("Chat")
elif tab == "Airtable":
	st.write("Vision")
elif tab == "Manual":
	st.write("Snowflake")

