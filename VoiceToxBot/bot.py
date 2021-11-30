import os
import pandas

import discord
from dotenv import load_dotenv

THRESHOLD = 0.8

df = pandas.read_csv('example.csv')
sorted_df = df.sort_values(by=['Tox_Score'], ascending=False)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    #moderator-only channel
    channel = client.get_channel(896922980800671767)
    
    for ind in sorted_df.index:
        score = sorted_df['Tox_Score'][ind]
        if score >= THRESHOLD:
            name = sorted_df['Username'][ind]
            discriminator = sorted_df['Discriminator'][ind]
            voice_channel = sorted_df['Channel_Name'][ind]
            message = f'Alert: User {name}{discriminator} has reached a toxicity score of {score} in voice channel {voice_channel}'
            await channel.send(message)

    

client.run(TOKEN)