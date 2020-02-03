import discord
import SECRETS
import settings
import yaml

timeChecker = 0

@settings.client.event
async def on_ready():
    # make sure the bot is running
    print("Ready!")
    await settings.client.change_presence(status=discord.Status.online, activity=discord.Game(name='ZeldaDonkeyDS - Post Edition'))
    # make sure the bot is connected to the server
    for s in settings.client.guilds:
        print(" - %s (%s)" % (s.name, s.id))

@settings.client.event
async def on_message(message):
    cmd = None
    byBot = message.author.bot
    if not byBot:
        if message.channel.id in settings.channel:
            content = message.content
            if len(message.attachments) > 0:
                image = message.attachments[0]
                content = content + "\n" + image.url
            name = message.author.name
            guild = message.guild.name
            new_message = "**"+name+"@"+guild+":** "+content
            channel = message.channel.id

            if len(message.attachments) < 1:
                msg = message.content.upper()
                try:
                    cmd = msg.split()[0]
                except:
                    cmd = msg

            if cmd == "!HELP":
                help_message = "Dieser Bot übermittelt aktuell Nachrichten von den folgenden Servern: \n"
                for s in settings.client.guilds:
                    help_message = help_message + "- " + s.name + "\n"
                await send_msg(message.channel, help_message)
            elif cmd == "!RELOADYAML":
                if message.author.id == 223871330603237376:
                    with open('channel.yml', 'rt', encoding='utf8') as yml:
                        settings.channel = yaml.load(yml, Loader=yaml.FullLoader)
                    with open('userblock.yml', 'rt', encoding='utf8') as yml:
                        settings.userblock = yaml.load(yml, Loader=yaml.FullLoader)
                    task = send_msg(message.channel, "Yaml updated successfully.")
                    await task
            else:
                if message.author.id in settings.userblock:
                    task = send_msg(message.channel, "{} Deine Nachricht wurde nicht weitergeleitet, da du auf der Blacklist stehst.".format(message.author.mention))
                    await task
                else:
                    f = open("userlog.txt", "a")
                    f.write("{}: {}\n".format(message.author.name, str(message.author.id)))
                    f.close()
                    for i in settings.channel:
                        if not i == channel:
                            try:
                                next_ch = settings.client.get_channel(i)
                                await send_msg(next_ch, new_message)
                            except:
                                pass

@settings.client.event
async def send_msg(channel, msg):
    if isinstance(msg, list):
        for m in msg:
            await channel.send(m)
    else:
        await channel.send(msg)

# initialize
settings.client.run(SECRETS.TOKEN)
