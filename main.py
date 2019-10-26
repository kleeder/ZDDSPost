import discord
import SECRETS
import settings
import yaml

timeChecker = 0

@settings.client.event
async def on_ready():
    # make sure the bot is running
    print("Ready!")
    await settings.client.change_presence(game=discord.Game(name='ZeldaDonkeyDS - Post Edition'))
    # make sure the bot is connected to the server
    for s in settings.client.servers:
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
                content = image.get('url')
            name = message.author.name
            server = message.server.name
            new_message = "**"+name+"@"+server+": **"+content
            channel = message.channel.id

            if len(message.attachments) < 1:
                msg = message.content.upper()
                try:
                    cmd = msg.split()[0]
                except:
                    cmd = msg

            if cmd == "!HELP":
                help_message = "Dieser Bot übermittelt aktuell Nachrichten von den folgenden Servern: \n"
                for s in settings.client.servers:
                    help_message = help_message + "- " + s.name + "\n"
                await send_msg(message.channel, help_message)
            elif cmd == "!RELOADCHANNEL":
                if message.user.id == "223871330603237376":
                    with open('channel.yml', 'rt', encoding='utf8') as yml:
                        settings.channel = yaml.load(yml)
                    task = send_msg(message.channel, "Channel updated successfully.")
                    await task
            else:
                for i in settings.channel:
                    if not i == channel:
                        try:
                            next_ch = settings.client.get_channel('{}'.format(i))
                            await send_msg(next_ch, new_message)
                        except:
                            pass

@settings.client.event
async def send_msg(channel, msg):
    if isinstance(msg, list):
        for m in msg:
            await settings.client.send_message(channel, m)
    else:
        await settings.client.send_message(channel, msg)

# initialize
settings.client.run(SECRETS.TOKEN)
