from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool

from dotenv import load_dotenv
load_dotenv()

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel()  # Uses a default model

# Create an agent with no tools
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
)

# Run the agent with a task
result = agent.run("What is the current weather in Paris?")
print(result)