
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
tab1, tab2, tab3, tab4 = st.tabs(["Local file", "Google sheets", "Airtable", "Snowflake"])
with tab1:
	uploaded_file = st.sidebar.file_uploader("Choose a file 📂", type=["csv"])
	if uploaded_file is None:
		st.error("Select a data source and upload a file to continue.", icon="🚨")
	if uploaded_file is not None:
		df = pd.read_csv(uploaded_file, encoding='latin-1')
		querydata = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)
		manual = st.sidebar.toggle("Enable manual plotting")
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
			user_input = st.text_area("Enter your input 💬", placeholder="Enter your question/query", height=200)  
			enter_button = st.button("Enter ⚡", use_container_width=True, type="primary")
			if enter_button:
				if user_input:
					with st.spinner():
						conv = querydata.query(user_input)
		with col4:
			with st.expander("👀 Analyse charts and graphs visually."):
				st.write("Sample")
			output = st.text_area("Your generated output 🎉", placeholder="The output will be displayed here", value=conv if 'conv' in locals() else "", height=200)
			generate = st.button("Generate AI report ⚡", use_container_width=True)
			
		if generate:
			query_engine = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)
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
		if manual:
			chart_types = st.multiselect("Select Chart Types", ["Bar Chart", "Stacked Bar Chart","Line Chart", "Scatter Plot", "Pie Chart", "Dot Plot", "Histogram", "Area Chart"])
			for chart_type in chart_types:
				st.subheader(f"{chart_type} Visualization")
				if chart_type == "Area Chart":
					st.sidebar.write("Select attributes for Filled Area Chart")
					x_axis = st.sidebar.selectbox("Select for Area Chart - X", df.columns, key=f"area_x_{chart_type}", index=None)
					y_axis = st.sidebar.selectbox("Select for Area Chart - Y", df.columns, key=f"area_y_{chart_type}", index=None)
                    			color = st.sidebar.selectbox("Select Colour Column", df.columns, key=f"area_c_{chart_type}", index=None)
                    			line = st.sidebar.selectbox("Select Line Column", df.columns, key=f"area_l_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis is None or y_axis is None or color is None or line is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
					else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis)
                            				fig = px.area(df_sort, x=x_axis, y=y_axis, color=color, line_group=line,title="Stacked filled area chart comparing sales with product line against order dates.", width=1240)
                            				st.plotly_chart(fig)
                        				st.toast('Graph visualized!', icon='🎉')
                    
                		elif chart_type == "Histogram":
					st.sidebar.write("Select X-axis and Y-axis for Histogram Chart")
                    			x_axis = st.sidebar.selectbox("Select for Bar Chart - X", df.columns, key=f"hist_x_{chart_type}", index=None)
                    			color = st.sidebar.selectbox("Select Colour Column", df.columns, key=f"hist_y_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis is None or color is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                    			else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis)
                            				fig = px.histogram(df_sort, x=x_axis, color=color, title='Order Status Distribution Over Time', width=1240)
                            				st.plotly_chart(fig)
                        				st.toast('Hooray!', icon='🎉')
                		elif chart_type == "Bar Chart":
					st.sidebar.write("Select X-axis and Y-axis for Bar Chart")
                    			x_axis = st.sidebar.selectbox("Select for Bar Chart - X", df.columns, key=f"bar_x_{chart_type}", index=None)
                    			y_axis = st.sidebar.selectbox("Select for Bar Chart - Y", df.columns, key=f"bar_y_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis is None or y_axis is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                   			else:
						with st.spinner("Generating chart..."):
                            			df_sort = df.sort_values(by=x_axis)
                            			fig = px.bar(df_sort, x=x_axis, y=y_axis, width=1240)
                            			st.plotly_chart(fig)
                        			st.toast('We did it!', icon='🎉')
						
                		elif chart_type == "Line Chart":
					st.sidebar.write("Select X-axis and Y-axis for Line Chart")
                    			x_axis1 = st.sidebar.selectbox("Select for Line Chart - X", df.columns, key=f"line_x_{chart_type}", index=None)
                    			y_axis1 = st.sidebar.selectbox("Select for Line Chart - Y", df.columns, key=f"line_y_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis1 is None or y_axis1 is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                    			else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis1)
                            				fig = px.line(df_sort, x=x_axis1, y=y_axis1, width=1240)
                            				st.plotly_chart(fig)
                        				st.toast('Hooray!', icon='🎉')
                		elif chart_type == "Scatter Plot":
					st.sidebar.write("Select X-axis and Y-axis for Scatter Plot Chart")
                    			x_axis3 = st.sidebar.selectbox("Select for Scatter Plot - X", df.columns, key=f"scatter_x_{chart_type}", index=None)
                    			y_axis3 = st.sidebar.selectbox("Select for Scatter Plot - Y", df.columns, key=f"scatter_y_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis3 is None or y_axis3 is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                    			else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis3)
                            				fig = px.scatter(df_sort, x=x_axis3, y=y_axis3, width=1240)
                            				st.plotly_chart(fig)
                        				st.toast('Another victory', icon='🥇')
                		elif chart_type == "Pie Chart":
					selected_column = st.sidebar.selectbox("Select Column for Pie Chart", df.columns, key=f"pie_column_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			with st.spinner("Generating chart..."):
						fig = px.pie(df, names=selected_column, title=f'Pie Chart for {selected_column}', width=1240)
                        			st.plotly_chart(fig)
                    				st.toast('Winning streak!', icon='🏆')
                		elif chart_type == "Stacked Bar Chart":
					st.sidebar.write("Select X-axis and Y-axis for Bubble Chart")
                    			x_axis4 = st.sidebar.selectbox("Select for Stacked Bar Chart - X", df.columns, key=f"stacked_x_{chart_type}", index=None)
                    			y_axis4 = st.sidebar.selectbox("Select for Stacked Bar Chart - Y", df.columns, key=f"stacked_y_{chart_type}", index=None)
                    			color = st.sidebar.selectbox("Select Color Column", df.columns, key=f"stacked_size_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis4 is None or y_axis4 is None or color is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                    			else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis4)
                            				fig = px.bar(df_sort, x=x_axis4, y=y_axis4, color=color, title=f'Stacked Bar Chart for {x_axis4}, {y_axis4}, {color}', width=1240)
                            				st.plotly_chart(fig)
                       					st.toast('Bubbles and soap!', icon='🧼')
                		elif chart_type == "Dot Plot":
					st.sidebar.write("Select X-axis and Y-axis for Dot Plot Chart")
                    			x_axis5 = st.sidebar.selectbox("Select for Dot Plot Chart - X", df.columns, key=f"dot_x_{chart_type}", index=None)
                    			y_axis5 = st.sidebar.selectbox("Select for Dot Plot Chart - Y", df.columns, key=f"dot_y_{chart_type}", index=None)
                    			st.sidebar.divider()
                    			if x_axis5 is None or y_axis5 is None:
						st.error("Either cant build relationship with given columns or Column(s) are empty")
                    			else:
						with st.spinner("Generating chart..."):
							df_sort = df.sort_values(by=x_axis5)
                            				fig = px.scatter(df_sort, x=x_axis5, y=y_axis5, title=f'Dot Plot for {x_axis5} and {y_axis5}', width=1240)
                            				st.plotly_chart(fig)
                        				st.toast('Hooray!', icon='🎉')
        
with tab2:
    st.warning("Google sheets integration is not avilable in Beta Version", icon="⚠")

with tab3:
    st.warning("Airtable integration is not avilable in Beta Version", icon="⚠")
        
with tab4:
    st.warning("Snowflake integration is not avilable in Beta Version", icon="⚠")

