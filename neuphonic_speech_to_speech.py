import os
import asyncio

from pyneuphonic import Neuphonic, Agent, AgentConfig

api_key = "" # GET THIS FROM beta.neuphonic.com!!!!!!!!!

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
