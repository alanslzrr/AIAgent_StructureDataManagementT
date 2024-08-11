import os
from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.tools.json.tool import JsonSpec
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def query_json_agent(agent, query):
    try:
        response = agent.invoke(query)
        return response['output'] if isinstance(response, dict) and 'output' in response else response
    except Exception as e:
        return f"Error: {str(e)}"
 #Setup JSON agenT with OpenAI
 
def setup_json_agent(data):
    spec = JsonSpec(dict_=data, max_value_length=4000)
    toolkit = JsonToolkit(spec=spec)
    return create_json_agent(
        llm=ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv('OPENAI_API_KEY')),
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True
    )


 