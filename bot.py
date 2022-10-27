import discord
from discord.ext import tasks,commands
import  requests
import conf
bot = discord.Client()
bot = commands.Bot(command_prefix=".")
host=conf.HOST
async def on_ready():
    print("Bot ready")

@tasks.loop(minutes = 100)
async def notify():
    url = host+'/apiDiscordNotifications'
    try:
        r = requests.get(url = url,verify=False)
        data = r.json()
        for i in data:
            await sendNotification(i,data[i]["discordId"],data[i]["reader"],data[i]["link"],data[i]["author"])
    except:
        print("check host")

@bot.command()
async def connectETD(ctx, *args):
    await ctx.send(f"Your ID: `{ctx.author.id}`")

@bot.command()
async def ping(ctx):
    await ctx.send(f'My ping is** {round(bot.latency*1000)} Ms**')


async def sendNotification(id,id_user,reader,content,author):
    if(id_user):
        user = await bot.fetch_user(id_user)
        message="A new notification for "+reader+" on this link: "+content+"\nby "+author
        await user.send(message)
        burnNotification(id)

def burnNotification(id):
    url = host+'/apiDiscordBurnNotification'
    target={"id":id}
    r = requests.get(url = url,params=target,verify=False)
    response = r.json()
notify.start()
bot.run(conf.BOT_KEY)