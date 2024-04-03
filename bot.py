import discord
import os  # default module
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file
bot = discord.AutoShardedBot(intents=discord.Intents.all())

# Events handling
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    # send response to the user, only the user can see the response
    await ctx.response.send_message("Hey!", ephemeral=True)

connections = {}


# Our voice client already passes these in.
async def once_done(sink: discord.sinks, *args):
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()  # Disconnect from the voice channel.

    # Save audio data to a file.
    for user_id, audio in sink.audio_data.items():
        with open(f"{user_id}.{sink.encoding}", "wb") as f:
            f.write(audio.file.getbuffer())
    


@bot.command()
async def record(ctx):  # If you're using commands.Bot, this will also work.
    # if not owner, return
    if str(ctx.author.id) != str(os.getenv('OWNER_ID')):
        return await ctx.response.send_message("You thought you could use this command? Think again!", ephemeral=True)
    
    voice = ctx.author.voice

    if not voice:
        await ctx.response.send_message("You aren't in a voice channel!", ephemeral=True) 

    # Connect to the voice channel the author is in.
    vc = await voice.channel.connect()
    # Updating the cache with the guild and channel.
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        discord.sinks.MP3Sink(),  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )
    await ctx.response.send_message("Started recording!", ephemeral=True)


@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        # Stop recording, and call the callback (once_done).
        vc.stop_recording()
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        # Respond with this if we aren't recording.
        await ctx.response.send_message("I am currently not recording here.", ephemeral=True)

# handle direct messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        if message.author.id != int(os.getenv('MAIN_BOT_ID')):
            return

    await bot.process_commands(message)



bot.run(str(os.getenv('DISCORD_TOKEN')))  # run the bot with the token
