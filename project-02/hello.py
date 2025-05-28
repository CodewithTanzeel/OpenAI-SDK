import os
import chainlit as cl
from agents import Agent,RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url ="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client = provider,
)
# Config At the run LEVEL
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Step #3
agent1 = Agent(
        name="Computer Hardware Expert",
        instructions="You are helpful Assitant that can answer question to Any computer hardware questions.",
        model=model,

    )

@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(
        agent1,
        input = message.content,
        run_config = run_config, 
    )
    await cl.Message(content=result.final_output).send()