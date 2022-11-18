import discord
from discord.ext import tasks,commands
import  requests
import conf
bot = discord.Client()
bot = commands.Bot(command_prefix=".")
host=conf.HOST

async def on_ready():
    print("Bot ready")

if host:
    @tasks.loop(minutes = 1)
    async def notify():
        url = host+'/apiDiscordNotifications/key='+conf.SECURITY_KEY
        try:
            data = sendRequest(url)
            for i in data:
                await sendNotification(i,data[i]["discordId"],data[i]["reader"],data[i]["link"],data[i]["author"])
        except Exception as e:
            print(e)
    @tasks.loop(hours = 24)
    async def reminder():
        url = host+'/apiTasks/key='+conf.SECURITY_KEY
        users={}
        try:
            data = sendRequest(url)
            print(data)
            for i in data:
                if data[i]["discordId"] in users:
                    users[data[i]["discordId"]]+=[{"title":data[i]["title"],"link":data[i]["link"]}]
                else:
                    users[data[i]["discordId"]]=[{"title":data[i]["title"],"link":data[i]["link"]}]
            await sendReminder(users)
        except Exception as e:
            print(e)
    reminder.start()
    notify.start()
    
@bot.command()
async def connectETD(ctx, *args):
    await ctx.send(f"Your ID: `{ctx.author.id}`")

@bot.command()
async def ping(ctx):
    await ctx.send(f'My ping is** {round(bot.latency*1000)} Ms**')

@bot.command()
async def myTasks(ctx):
    target=ctx.author.id
    url = host+'/apiTasks/key='+conf.SECURITY_KEY
    response=sendRequest(url)
    data=[]
    message="Hello there :wine_glass:.\nThere are:\n"
    for i in response:
        print(i)
        if str(i).endswith(str(target)):
            message+="\n:bar_chart: **"+ response[i]["title"]+"** link:"+response[i]["link"]+"\n"
    message+="\nGood Luck :heart:"
    await ctx.send(message)

async def sendNotification(id,id_user,reader,content,author):
    if(id_user):
        try:
            user = await bot.fetch_user(id_user)
            message="A new notification for "+reader+" on this link: "+content+"\nby "+author
            await user.send(message)
            burnNotification(id)
        except:
            print("id don't work")

async def sendReminder(data):
    for i in data:
        message="Hello there :wine_glass:.\nFor today, we have the following to do:\n"
        for j in data[i]:
            message+="\n:bar_chart: **"+ j["title"]+"** link:"+j["link"]+"\n"
        message+="\nGood Luck :heart:"
        if(data[i]):
            try:
                user = await bot.fetch_user(i)
                await user.send(message)
            except:
                print("id don't work")
def burnNotification(id):
    url = host+'/apiDiscordBurnNotification/key='+conf.SECURITY_KEY
    target={"id":id}
    sendRequest(url,target)


def sendRequest(url,request=None):
    r = requests.get(url = url, params=request, verify=False)
    response = r.json()
    return response

bot.run(conf.BOT_KEY)