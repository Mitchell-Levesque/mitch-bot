import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup
from timeit import default_timer as timer

# Simply utility function for bolding strings according to Discord's syntax
def bold(message: str) -> str:
  return "**"+message+"**"

def italics(message: str) -> str:
  return "_"+message+"_"

#Discord Bot Token
token = 'NDQ0OTkyNDcyMjA5NDI0Mzg0.XjiJKA.fNH1C5KsFnn2T16QemUU43HVdpE'

# Create bot instance with prefix !
client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Command for looking up summoner names on North American server
@bot.command(name='opgg')
async def opgg(ctx, *, summoner: str):
  try:
    # Start timer for function
    start = timer()

    # Get html for the na.op.gg page
    url = 'https://na.op.gg/summoner/userName=' + summoner
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find summoner name and rank
    summoner = soup.find(class_='Name').get_text().strip()
    rank = soup.find(class_='TierRank').get_text().strip()
    
    # If the player is ranked, then get LP and win/loss record
    if(rank != 'Unranked'):
      lp = soup.find(class_='LeaguePoints').get_text().strip()
      ranklbl = rank + ", " + lp
      wins = soup.find(class_='wins').get_text().strip()
      losses = soup.find(class_='losses').get_text().strip()
      winrate = soup.find(class_='winratio').get_text().strip()
      winlosslbl = wins+"/"+losses+", "+winrate
    # If the player is unranked, then ignore LP and set 0W/0L record
    else:
      ranklbl = rank
      winlosslbl = "0W/0L, Win Ratio 0%"
    
  # If an exception is thrown, the summoner does not exist
  except:
    await ctx.send("Summoner does not exist.")
    return
  
  # Make embed message with orange color
  embed = discord.Embed(
    colour = discord.Color.dark_orange()
  )

  # Set the icon depending on tier the player is
  if('Challenger' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Challenger_1.png')
    ranklbl = "<:challenger:691812452412948502>" + ranklbl
  elif('Grandmaster' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Grandmaster_1.png')
    ranklbl = "<:grandmaster:691812452895162419>" + ranklbl
  elif('Master' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Master_1.png')
    ranklbl = "<:master:691812453016666195>" + ranklbl
  elif('Diamond' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Diamond_1.png')
    ranklbl = "<:diamond:691812452945625129>" + ranklbl
  elif('Platinum' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Platinum_1.png')
    ranklbl = "<:plat:691812452857413665>" + ranklbl
  elif('Gold' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Gold_1.png')
    ranklbl = "<:gold:691812452760813639>" + ranklbl
  elif('Silver' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Silver_1.png')
    ranklbl = "<:silver:691812452865802291>" + ranklbl
  elif('Bronze' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Bronze_1.png')
    ranklbl = "<:bronze:691812451930603642>" + ranklbl
  elif('Iron' in rank):
    embed.set_thumbnail(url='https://img.rankedboost.com/wp-content/uploads/2014/09/Season_2019_-_Iron_1.png')
    ranklbl = "<:iron:691812452639178773>" + ranklbl
  elif('Unranked' in rank):
    embed.set_thumbnail(url='https://opgg-static.akamaized.net/images/medals/default.png?image=q_auto&v=1')
    ranklbl = "<:unranked:691812452383457390>" + ranklbl


  # We have 3 rows, Summoner name, Rank and Win ratio.  Place these values
  embed.add_field(name='Summoner', value=bold(summoner)+" (NA)", inline=False)
  embed.add_field(name='Rank', value=ranklbl, inline=False)
  embed.add_field(name='Win/Loss', value=winlosslbl, inline=False)

  # Stop the timer for the function, and place footer message including time the lookup took, and author's discord tag
  end = timer()
  embed.set_footer(text="This lookup took %0.2f seconds.\nMade by Aalmost#5337" % (end-start))
  await ctx.send(embed=embed)

# Command used to easily exit the bot
# Only available to owner
@bot.command(name='quit')
@commands.is_owner()
async def quit(ctx):
  await ctx.send("Bot exitted")
  await ctx.bot.logout()

bot.run(token)