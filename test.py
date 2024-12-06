from pyneuphonic import Neuphonic, WebsocketEvents
from pyneuphonic.player import AsyncAudioPlayer, AsyncAudioRecorder
from pyneuphonic.models import APIResponse, AgentResponse, AgentConfig
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

import os
import asyncio


async def main():
    transcript = ""
    client = Neuphonic(api_key="172c4d78863aec707d4496f0d5258bff3389e92b2614c8175e7f18575eebc4a5.f13b6de5-100a-4252-b2fd-7a4aa39c852f")

    ws = client.agents.AsyncWebsocketClient()
    player = AsyncAudioPlayer()

    # passing in the websocket object will automatically forward audio to the server
    recorder = AsyncAudioRecorder(websocket=ws)

    async def on_message(message: APIResponse[AgentResponse]):
        transcript = ""
        # server will return 3 types of messages: audio_response, user_transcript, llm_response
        if message.data.type == 'audio_response':
            await player.play(message.data.audio)
        elif message.data.type == 'user_transcript':
            print(f'User: {message.data.text}')
            transcript += message.data.text
        elif message.data.type == 'llm_response':
            print(f'Agent: {message.data.text}')

    async def on_close():
        await player.close()
        await recorder.close()

    ws.on(WebsocketEvents.MESSAGE, on_message)
    ws.on(WebsocketEvents.CLOSE, on_close)

    await player.open()
    await ws.open(AgentConfig(endpointing=500))
    await recorder.record()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await ws.close()

    # Load tokenizer and model
    tokenizer = LlamaTokenizer.from_pretrained("path_to_weights")
    model = LlamaForCausalLM.from_pretrained("path_to_weights")
    input_text = "Find the food item in this respective phrase and print it: "+transcript
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=50)
    print(tokenizer.decode(outputs[0]))


asyncio.run(main())

