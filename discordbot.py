from timeit import default_timer as timer

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

import mytoken
import utility

# Global variable for tracking current op.gg lookup region (default NA)
cur_region = 'NA'
# List of possible regions
regions = ['NA', 'EUW', 'KR', 'EUNE', 'JP', 'OCE', 'BR', 'LAS', 'LAN', 'RU', 'TR']

# Discord Bot Token
token = mytoken.token

# Create bot instance with prefix !
client = discord.Client()
bot = commands.Bot(command_prefix='!')
# Remove existing help command
bot.remove_command("help")

# Set discord status on ready
@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.mro, activity=discord.Game('!help'))

# Command for switching op.gg lookup region (bot on NA)
@bot.command(name='region')
async def region(ctx, rg: str='None'):
  global cur_region
  if(rg == 'None'):
    await ctx.send("Current region: %s" % cur_region)
  else:
    rg = rg.upper()
    if(rg in regions):
      cur_region = rg
      await ctx.send("Region has been switched to %s." % cur_region)
    else:
      await ctx.send("Region %s is undefined." % rg)
  
# Command for looking up summoner names on North American server
@bot.command(name='opgg')
async def opgg(ctx, *, summoner: str):
  try:
    # Start timer for function
    start = timer()

    # Send loading message
    embed = discord.Embed(
      color = discord.Color.orange()
    )
    embed.title = 'Loading...'
    embed.set_thumbnail(url='https://www.easypestcontrol.in/js/loaderimg.gif')
    message = await ctx.send(embed=embed)

    # Get url for the op.gg page depending on region
    if(region == 'KR'):
      url = 'https://www.op.gg/summoner/userName=%s' % summoner
    else:
      url = 'https://%s.op.gg/summoner/userName=%s' % (cur_region, summoner)
    
    # Get html from the url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find summoner name and rank
    names = soup.find_all(class_='Name')
    summoner = names[0].get_text().strip()
    # If the first name returned contains "[", then it means it was a pro player on op.gg.
    # So, it's actually the second name instance which is their summoner name
    if('[' in summoner):
      summoner = names[1].get_text().strip()
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
    await discord.Message.delete(message)
    await ctx.send("Summoner does not exist.\nRegion: %s" % cur_region)
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
  embed.add_field(name='Summoner', value=utility.bold(summoner)+" (%s)"%cur_region, inline=False)
  embed.add_field(name='Rank', value=ranklbl, inline=False)
  embed.add_field(name='Win/Loss', value=winlosslbl, inline=False)

  # Stop the timer for the function, and place footer message including time the lookup took, and author's discord tag
  end = timer()
  embed.set_footer(text="Data taken from OP.GG\nThis lookup took %0.2f seconds." % (end-start), 
                  icon_url='https://static-s.aa-cdn.net/img/gp/20600001273372/UdvXlkugn0bJcwiDkqHKG5IElodmv-oL4kHlNAklSA2sdlVWhojsZKaPE-qFPueiZg=s300')

  # Delete loading message and then send embed message
  await discord.Message.delete(message)
  await ctx.send(embed=embed)

@bot.command(name='help')
async def help(ctx):
  embed = discord.Embed(
    color = discord.Color.dark_orange()
  )

  embed.set_footer(text="Any problems? Contact Aalmost#5337")

  await ctx.send(embed=embed)

# Command used to easily exit the bot
# Only available to owner
@bot.command(name='quit')
@commands.is_owner()
async def quit(ctx):
  await ctx.send("Bot exitted")
  await ctx.bot.logout()

bot.run(token)
