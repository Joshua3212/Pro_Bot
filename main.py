import discord
import asyncio
import random
from discord.ext import commands
import requests
#Translator
from googletrans import Translator
import texte
from texte import SPRACHEN,HELP



TAG = "[L O L] "
TOKEN = "NTM4MDI1ODgxNDkxMjEwMjQw.D0xCjw.Csdc_I-LpaS6y1zQVX2wRLVN3cs"

bot = commands.Bot(
    command_prefix="-"
)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_member_join(member):
    await tag(member)


@bot.event
async def on_member_update(before, after: discord.Member):
    if after.status != before.status:
        await tag(after)


async def tag(member):
    try:
        print(member)
        if not member.display_name.startswith(TAG):
            await bot.change_nickname(member, (TAG + member.name)[:32])
            return True
    except Exception as e:
        print(e)
    return False


# commands
@bot.command(pass_context=True)
async def tag_all(ctx: commands.Context):
    members = [member for member in ctx.message.server.members]
    count = 0
    for m in members:
        if not m.bot:
            if await tag(m):
                count += 1
            await asyncio.sleep(0.3)
    await bot.say("Done. {} getaggt".format(count))

@bot.command()
async def rtm():
    msg = 'http://surviv.io/?region=eu&zone=rtm \nhttps://surviv.io/?region=eu&zone=rtm'
    await bot.say(msg)

@bot.command()
async def fr():
    msg = 'http://surviv.io/?region=eu&zone=fr \nhttps://surviv.io/?region=eu&zone=fr'
    await bot.say(msg)

@bot.command(pass_context=True)
async def languages(ctx):
    ...
    ...
    await bot.send_message(ctx.message.author, SPRACHEN)
#nachricht im channel
    msg = "Please check your DMs :white_check_mark: "
    await bot.say(msg)

@bot.command(pass_context=True)
async def helpme(ctx):
    ...
    ...
    await bot.send_message(ctx.message.author, HELP)
#nachricht im channel
    msg = "Please check your DMs :white_check_mark: "
    await bot.say(msg)

@bot.command(pass_context=True)
async def ping(ctx: commands.Context):
    msg = 'pong  {0.author.mention}'.format(ctx.message)
    await bot.say(msg)

@bot.command()
async def translate(*, query):
    translator = Translator()
    msg = translator.translate(query)
    await bot.say(msg.text)

@bot.command()
async def translatefromto(src, dest, *, query):
    translator = Translator()
    msg = translator.translate(query, src=src, dest=dest)
    await bot.say(msg.text)

@bot.command()
async def MEE6():
    msg = "https://cdn.discordapp.com/attachments/529625690132316169/547130590479122453/RichNoobMEE6.png"
    await bot.say(msg)

@bot.command()
async def uptime():
    msg = 'I am up when I am online dude :grin:'
    await bot.say(msg)

@bot.command(pass_context=True)
async def ProBot(ctx: commands.Context):
    msg = 'aww do u like me ? -yes :thumbsup: or -no :thumbsdown: ?'
    await bot.say(msg)
    try:
        answer = await bot.wait_for_message(timeout=60.0, author=ctx.message.author).content.lower()
        if answer in ["yes", "ja", ":thumbsup:"]:
            msg = 'aww thx I will tell ShopOwner to add a bit of money to u (he is my friend :joy:)'
        elif answer in ["no", "nein", ":thumbsdown:"]:
            msg = ':sob: :sob: I will tell MEE6 to ban u :sob:'
        else:
            msg = "Not sure about that answer :thinking:"
        await bot.say(msg)
    except:
        pass
# lottery
@bot.command(pass_context=True)
async def lottery(ctx: commands.Context):
    await bot.say('Guess a number between 1 to 30')

    def guess_check(m):
        return m.content.isdigit()

    guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)
    answer = random.randint(1, 30)
    if guess is None:
        fmt = 'Sorry, you took too long. It was {}.'
        await bot.say(fmt.format(answer))
        return
    if int(guess.content) == answer:
        await bot.say('You are right !(please send a screenshot of this text as quickly as possible to a mod )')
    else:
        await bot.say('Sorry. It is actually {}.'.format(answer))

# responses
@bot.event
async def on_message(message):
    print(message.content)
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith('.'):
        msg = 'stop using ..... Noone does use that :rage:'.format(message)
        await bot.send_message(message.channel, msg)

    if message.content.startswith('@!538025881491210240'):
        msg = 'hmm {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

    if message.content.startswith("<@!538025881491210240>"):
        msg = 'whuuut ? {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

    if message.content.startswith("anyone"):
        msg = "maybye you will find someone if you ping **__@lfg__**"
        await bot.send_message(message.channel, msg)

    await bot.process_commands(message)

#Vc
@bot.command(pass_context=True)
async def teams(ctx: commands.Context, channel_name: str, team_size: int):
    if team_size != 2 and team_size != 4:
        await bot.say("Teamsize has to be 2 or 4")
        return
    channels = ctx.message.server.channels
    vc = [c for c in channels if c.name.startswith(channel_name) and c.type == discord.ChannelType.voice]
    if not vc:
        await bot.say("Voicechannel '{}' not found".format(channel_name))
        return
    vc = vc[0]
    members = vc.voice_members
    if len(members) % team_size != 0:
        await bot.say("{} is not divisible by {}".format(len(members), team_size))
    team_order = [i for i in range(len(members))]
    random.shuffle(team_order)

    team_order = [team_order[i*team_size : (i+1)*team_size] for i in range(len(members)//team_size)]
    teams = []
    for t in team_order:
        teams.append([members[i] for i in t])

    for team in teams:
        c = await bot.create_channel(ctx.message.server, "Team {}".format("|".join([m.display_name for m in team])), type=discord.ChannelType.voice)
        await asyncio.sleep(0.2)
        for m in team:
            await bot.move_member(m, c)


bot.run(TOKEN)
