from discord import Client, errors
import sys

client = Client()
@client.event
async def on_ready():
    await client.close()
try:
    client.run(sys.argv[1])
    exit(0)
except errors.LoginFailure:
    exit(1)