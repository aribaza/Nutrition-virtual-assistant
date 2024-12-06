import os
import asyncio

from pyneuphonic import Neuphonic, Agent, AgentConfig

api_key = "172c4d78863aec707d4496f0d5258bff3389e92b2614c8175e7f18575eebc4a5.f13b6de5-100a-4252-b2fd-7a4aa39c852f"

async def main():
    client = Neuphonic(api_key=api_key)

    agent_id = client.agents.create(
        name='Agent 1',
        prompt='You are a helpful agent. Answer in 10 words or less.',
        greeting='Hi, how can I help you today?'
    )['data']['id']

    agent = Agent(client, agent_id=agent_id, tts_model='neu_hq')

    await agent.start()
asyncio.run(main())
