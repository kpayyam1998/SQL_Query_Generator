import streamlit as st
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()

#key configure
key=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

#model
model=genai.GenerativeModel(model_name="gemini-pro")


def main():
    st.set_page_config(page_title="SQL Query Generator")
    st.markdown(
    """
        <div style="text-align:center;">
            <h1>SQL query generator</h1>
            <h3>I can generate sql queried for you</h3>
            <h4>With explanations as well</h4>
            <p>This tool is very simple tool that allows you to generate SQL queries based on your prompts.</p>

    """,
    unsafe_allow_html=True

    )
    prompt=st.text_area("Enter your prompt here")
    submit= st.button("Generate SQL query")
    if submit:
        with st.spinner("Generating sql query"):

            templete='''

            Create SQL Query using below condition:\n
            ######################################

            {prompt}

            ######################################

            I just want SQL query only
            
            '''

            formatted_template=templete.format(prompt=prompt)
            response=model.generate_content(formatted_template)

            sql_query=response.text.strip().lstrip("```sql").rstrip("```")

            st.write(sql_query)

            expected_output="""
            Can you please provoide the sample expected output for  below query:
            ###############################################################
            ```
            {sql_query}

            ```
            ###############################################################

            Provoide the results in table format...

            """

            expected_template=expected_output.format(sql_query=sql_query)
            expected_response=model.generate_content(expected_template)
            expected_result=expected_response.text
            #st.write(expected_result)

            # Explanation
            explained_query="""
            Explain the SQL Query:
            ###############################################################
            ```
            {sql_query}

            ```
            ###############################################################

            """

            explained_template=explained_query.format(sql_query=sql_query)
            explained_response=model.generate_content(explained_template)
            explained_result=explained_response.text
            #st.write(explained_result)

            # Results display for every successfull command
            with st.container():
                st.success("SQL Query generated successfully.Here is code below..")
                st.code(sql_query,language='sql')
                
                st.success("Expected output for the above query is below..")
                st.markdown(expected_result)

                st.success("Explanation for the above query is below..")
                st.markdown(explained_result)

            
main()