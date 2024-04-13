from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

key=os.getenv('OPENAI_API_KEY')
llm = OpenAI(temperature=0.5, openai_api_key=key)

# Generate SQL query

def generate_response(prompt):
    template_style="""
        Create SQL query for the following prompt:
        ########################################### 
        \n:{prompt}

        i just want SQL query only...

        """
    prompt_template = PromptTemplate(
        input_variables=["prompt"],
        template=template_style,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template,output_key="sql_query")
    return llm_chain({"prompt":prompt})

# Example table 
def generate_example(SQL_Query):
    template_query="""
    Provide example/sample data in table format below query:\n

    {SQL_Query}

    """

    template=PromptTemplate(input_variables=["SQL_Query"],
                            template=template_query)
    explained_chain=LLMChain(llm=llm,prompt=template,output_key="table_format")
    response=explained_chain({"SQL_Query":SQL_Query})

    return response

#Explanation
def generate_explantion(SQL_Query):
    template_query="""
    Explain the below query with 200 words:\n

    {SQL_Query}

    """

    template=PromptTemplate(input_variables=["SQL_Query"],
                            template=template_query)
    explained_chain=LLMChain(llm=llm,prompt=template,output_key="explained")
    response=explained_chain({"SQL_Query":SQL_Query})

    return response


st.set_page_config(page_title="SQL Query Generator using OPEN AI", page_icon=":robot_face:")
st.title("")
st.markdown("""<h1 style='text-align: center;'>SQL query generator</h1>
               <h3 style='text-align: center;'>I can generate sql queried for you</h3>
               <h4 style='text-align: center;'> With explanations as well</h4>
               <p>This tool is very simple tool that allows you to generate SQL queries based on your prompts.</p>
            """, unsafe_allow_html=True)
            

qry_prompt=st.text_area("Write condition:")

submit=st.button("Generate SQL query")

if submit:
    st.spinner("Generating sql query")
    
    with st.container():
        response=generate_response(qry_prompt)
        st.success("SQL query")
        query=response['sql_query']
        st.code(query)

        st.success("Example table")
        sample_explanation=generate_example(query)
        st.markdown(sample_explanation['table_format'])

        st.success("Explanation")
        explanation=generate_explantion(query)
        st.markdown(explanation['explained'])

