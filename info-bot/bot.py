import config
import json
import requests
import urllib
import wikipedia

from discord import Embed
from discord.ext import commands
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=config.NewsApiToken)

bot = commands.Bot(command_prefix='$')

@bot.command()
async def news(ctx, *source):
    """Query news via https://newsapi.org/

    Arguments:
    source -- string corresponding to newsapi source
    """
    source = source[0] if len(source) > 0 else "bbc-news"
    try:
        async with ctx.channel.typing():
            headlines = newsapi.get_top_headlines(sources=source)["articles"]
    except:
        await ctx.send("Whoopsie daisy! I can't seem to find my newspaper.")
        raise

    embed_message = Embed(title="Top Headlines")
    embed_message.set_author(name=source)
    # embed_message.set_author(name="BBC News", url="https://www.bbc.com/")
    # embed_message.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/BBC.svg/300px-BBC.svg.png")
    for h in headlines:
        blurb = "{0}\n{1}".format(h["url"], h["description"])
        embed_message.add_field(name=h["title"], value=blurb)

    await ctx.send(embed=embed_message)

@bot.command()
async def rules(ctx):
    """Define the rules of conversation"""
    await ctx.send("The rules of conversation are, in general, not to dwell on any one subject, but to pass lightly from one to another without effort and without affectation; to know how to speak about trivial topics as well as serious ones;")

@bot.command()
async def wiki(ctx, *page):
    """Query wikipedia

    Arguments:
    page -- name of page (very sensitive, problematic)
    """
    try:
        async with ctx.channel.typing():
            sanitized_query = urllib.parse.quote(' '.join(page))
            result = wikipedia.page(sanitized_query)
    except:
        await ctx.send("Whoopsie daisy! I don't know what happened but whatever it was didn't work.")
        raise

    embed_message = Embed(title=result.title, description=result.summary[:500] + "...", url=result.url)
    if len(result.images) > 0:
        embed_message.set_thumbnail(url=result.images[0])

    await ctx.send(embed=embed_message)

@bot.command()
async def test(ctx):
    """Doggo"""
    embed_message = Embed(title="Test Embed", description="This is simply a test embed and nothing more.")
    embed_message.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bow_bow.jpg/160px-Bow_bow.jpg")
    await ctx.send(embed=embed_message)

@bot.command()
async def preach(ctx, *verses):
    """Query bible via https://bible-api.com/

    Arguments:
    verses -- name of book followed by chapter and verse
    """
    try:
        if len(verses) == 0:
            raise

        async with ctx.channel.typing():
            sanitized_query = urllib.parse.quote(' '.join(verses))
            response = requests.get('https://bible-api.com/' + sanitized_query)
            if response.status_code != 200:
                raise
    except:
        await ctx.send("Doh! I don't know that one.")
        raise

    text = response.json()['text']
    if len(text) > 1991:
        text = text[:1991] + "..."

    message = "```" + text + "```"

    await ctx.send(message)

bot.run(config.DiscordBotToken)
