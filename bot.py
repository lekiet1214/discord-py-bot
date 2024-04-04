# pylint: disable=line-too-long
"""
This script contains a Discord bot that can record audio from voice channels and respond to slash commands.

The bot uses the discord.py library and requires a Discord token to run.

Commands:
- /hello: Sends a greeting message to the bot.
- /record: Starts recording audio from the voice channel the user is in.
- /stop_recording: Stops recording audio.

Events:
- on_message: Handles direct messages sent to the bot.
- on_ready: Prints bot information when it is ready.
- on_voice_state_update: Handles voice channel disconnect events.

Dependencies:
- discord.py: A Python wrapper for the Discord API.
- dotenv: Loads environment variables from a .env file.

Note: This code assumes that the necessary environment variables are set in the .env file.
"""

import os
import discord
from dotenv import load_dotenv

load_dotenv()
bot = discord.AutoShardedBot(intents=discord.Intents.all())

# Slash command to say hello to the bot


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    """
    Sends a greeting message to the user who invoked the slash command.

    Parameters:
    - ctx: The context object representing the slash command invocation.
    """
    await ctx.response.send_message("Hey!", ephemeral=True)

connections = {}

# Callback function to handle recording completion


async def once_done(sink: discord.sinks):
    """
    Callback function to handle recording completion.

    Parameters:
    - sink: The sink object representing the audio recording.
    """
    await sink.vc.disconnect()

    for user_id, audio in sink.audio_data.items():
        with open(f"{user_id}.{sink.encoding}", "wb") as f:
            f.write(audio.file.getbuffer())

# Command to start recording audio


@bot.command()
async def record(ctx):
    """
    Starts recording audio from the voice channel the user is in.

    Parameters:
    - ctx: The context object representing the command invocation.
    """
    if str(ctx.author.id) != str(os.getenv('OWNER_ID')):
        return await ctx.response.send_message("You thought you could use this command? Think again!", ephemeral=True)

    voice = ctx.author.voice

    if not voice:
        await ctx.response.send_message("You aren't in a voice channel!", ephemeral=True)

    vc = await voice.channel.connect()
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        discord.sinks.MP3Sink(),
        once_done,
        ctx.channel
    )
    await ctx.response.send_message("Started recording!", ephemeral=True)

# Command to stop recording audio


@bot.command()
async def stop_recording(ctx):
    """
    Stops recording audio and deletes the recording.

    Parameters:
    - ctx: The context object representing the command invocation.
    """
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        vc.stop_recording()
        del connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.response.send_message("I am currently not recording here.", ephemeral=True)

# Event handler for direct messages


@bot.event
async def on_message(message):
    """
    Event handler for direct messages sent to the bot.

    Parameters:
    - message: The message object representing the direct message.
    """
    if message.author == bot.user:
        if message.author.id != int(os.getenv('MAIN_BOT_ID')):
            return

# Event handler for bot ready event


@bot.event
async def on_ready():
    """
    Event handler for the bot ready event.
    """
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Event handler for voice channel disconnect events


@bot.event
async def on_voice_state_update(member, before, after):
    """
    Event handler for voice channel disconnect events.

    Parameters:
    - member: The member object representing the user.
    - before: The voice state before the update.
    - after: The voice state after the update.
    """
    if member == bot.user:
        if before.channel and not after.channel:
            if member.guild.id in connections:
                del connections[member.guild.id]

bot.run(str(os.getenv('DISCORD_TOKEN')))
