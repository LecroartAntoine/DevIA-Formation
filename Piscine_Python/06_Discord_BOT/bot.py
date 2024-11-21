import discord, responses, datetime, asyncio, json
from discord.ext import commands
from urllib.request import Request, urlopen
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

channels = [1031888445607510090, 777636846829699116]

async def send_message(message, user_message, name):
    try:
        response = responses.handle_response(user_message, name)
        if response:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    bot = commands.Bot(command_prefix = '/', intents = intents)

    # async def daily_meme():
    #     while True:
    #         now = datetime.datetime.now()
    #         delta = datetime.timedelta(hours=now.hour, minutes = now.minute, seconds = now.second)
    #         when = datetime.timedelta(days  = 1, hours=7, minutes= 0, seconds = 0)
    #         await asyncio.sleep((when - delta).total_seconds())

    #         req = Request(url = 'https://meme-api.com/gimme/ProgrammerHumor', headers = {'User-Agent' : 'Mozilla/5.0'})
    #         response = urlopen(req)
    #         memeData = json.loads(response.read())
    #         meme = discord.Embed(title = "Daily meme", url = memeData['preview'][-1], description = memeData['title'], color = 0xF08080)
    #         meme.set_image(url = memeData['preview'][-1])

    #         for channel in channels:
    #             await bot.get_channel(channel).send(embed = meme)
            
    @bot.event

    async def on_ready():
        print(f'{bot.user} is now running !')
        # await daily_meme()


    @bot.event

    async def on_message(message):

        if message.author != bot.user:
        
            if message.author.nick == None:
                name = str(message.author)[:-5]
            else:
                name = str(message.author.nick)

            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{name} said: '{user_message}' ({channel})")

            await send_message(message, user_message, name)

            await bot.process_commands(message)

    @bot.command()
    async def meme(ctx, arg = None):
        try:
            req = Request(url = f'https://meme-api.com/gimme/{arg}', headers = {'User-Agent' : 'Mozilla/5.0'})
            response = urlopen(req)
            memeData = json.loads(response.read())
            meme = discord.Embed(title = "Meme sur demande:", url = memeData['preview'][-1], description = memeData['title'], color = 0xF08080)
            meme.set_image(url = memeData['preview'][-1])

            await ctx.send(embed = meme)

        except:
            await ctx.send('Subreddit introuvable')
    
    @bot.command()
    async def ethan(ctx):
        ethan = discord.Embed(title = "Le plus beau", color = 0xF08080)
        file = discord.File("/home/antoine-lecroart/Discord_BOT/Ethan.jpg", filename = "Ethan.jpg")
        ethan.set_image(url="attachment://Ethan.jpg")
        await ctx.send(file = file, embed = ethan)

    bot.run(TOKEN)