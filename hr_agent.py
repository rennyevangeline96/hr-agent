from dotenv import load_dotenv
load_dotenv()

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

agent = AssistantAgent(
    name="hr_assistant",
    model_client=model_client,
    system_message="You are an HR assistant.",
)


async def main():
    await Console(
        agent.run_stream(
            task=(
                "Write a job description for a Junior Python Developer in exactly 5 lines. "
                "Start with the job title as a heading, then give exactly 5 numbered lines, "
                "numbered 1 to 5, one short sentence each, covering responsibilities and requirements. "
                "No introduction and no closing text."
            )
        )
    )
    await model_client.close()


asyncio.run(main())