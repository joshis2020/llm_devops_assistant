# main.py
import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_aws import ChatBedrockConverse
import botocore.config # Import botocore.config



# Import tools and configuration from our new files
from tools.ec2_tools import all_ec2_tools
from config import AWS_REGION, BEDROCK_MODEL_ID

def setup_agent():
    """
    Sets up the LangChain agent with Bedrock LLM, memory, and tools.
    """
    bedrock_config = botocore.config.Config(
        retries={
            'max_attempts': 10,  # Increase max attempts to allow more retries
            'mode': 'standard'   # Use standard retry mode with exponential backoff
        },
        read_timeout=60,     # Increase read timeout (e.g., 60 seconds)
        connect_timeout=60   # Increase connect timeout (e.g., 60 seconds)
    )

    # Initialize Bedrock Chat Model using configurations
    llm = ChatBedrockConverse(
        model_id=BEDROCK_MODEL_ID,
        region_name=AWS_REGION, # Pass region explicitly
        temperature=0
    ) 

    # Setup conversational memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True) 

    # Define the prompt for the agent
    prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])


    # Create the agent
    agent = create_tool_calling_agent(llm, all_ec2_tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=all_ec2_tools, memory=memory, verbose=True)
    return agent_executor

def run_devops_assistant_demo():
    """
    Runs the interactive demo for the DevOps assistant.
    """
    agent_executor = setup_agent()

    print("Welcome to the EC2 DevOps Assistant Demo! Type 'exit' to quit.")
    print("----------------------------------------------------------------")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == 'exit':
            print("Exiting demo. Goodbye!")
            break

        try:
            # Invoke the agent with the user's input
            response = agent_executor.invoke({"input": user_input})
            print(f"Assistant: {response['output']}")
        except Exception as e:
            print(f"Assistant Error: An error occurred during processing: {e}")
            print("Please try again or rephrase your request.")

if __name__ == "__main__":
    run_devops_assistant_demo()