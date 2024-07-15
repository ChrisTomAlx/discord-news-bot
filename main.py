import discord 
from discord.ext import commands
import requests

intents = discord.Intents.all() 
intents.messages = True 

bot = commands.Bot(command_prefix='!', intents=intents) 
NEWS_API_KEY = '02af255ad6fc4c9d93266a5c1b5d6e9e' 
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines' 

@bot.event 
async def on_ready():     
    print(f'We have logged in as {bot.user}') 
    
# @bot.event 
# async def on_message(message):
#     if message.content == 'test':
#         await message.channel.send('Testing 1 2 3')
#     await bot.process_commands(message)

@bot.command(name='99') 
async def news(ctx, country: str = 'us'):     
    params = {         
        'apiKey': NEWS_API_KEY,         
        'country': country,         
        'category': 'general',         
        'pageSize': 5  # Number of news articles to fetch     
    }     
    response = requests.get(NEWS_API_URL, params=params)     
    data = response.json()     
    
    if data['status'] == 'ok':         
        articles = data['articles']         
        news_message = 'HAHA Works:\n\n'         
        for article in articles:             
            news_message += f"*{article['title']}*\n{article['description']}\n{article['url']}\n\n"         
        await ctx.send(news_message)    
    else:         
        await ctx.send('Sorry, I could not fetch the news.') 
        
bot.run('BOT-TOKEN')