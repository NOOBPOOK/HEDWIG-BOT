import nextcord
from nextcord.ui import Button, View, Select
from nextcord.utils import get
from nextcord.ext import commands
import datetime

intents = nextcord.Intents(messages=True, message_content=True, guilds=True, voice_states=True, members=True)
client = commands.Bot(command_prefix="#", help_command=None, intents=intents)

@client.event
async def on_ready():
    print("Bot just landed on the server!")

@client.command()
async def ticket(ctx):
    user = ctx.author
    guild = client.get_guild(955312929123729478)
    head = get(guild.roles, id=957967793599418398)#head boys role
    hog = get(guild.roles, id=955379554187374622)#hog roles

    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
        user: nextcord.PermissionOverwrite(read_messages=True),
        hog: nextcord.PermissionOverwrite(read_messages=True),
        head: nextcord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(str(user), overwrites=overwrites)
    await channel.send(f"|{user.mention}|{user}|{user.id}\nYou have opened a ticket.\n\nPlease state what concerns you have and be patient while we come to help you")
    view = View(timeout=None)
    button = Button(label="close", style=nextcord.ButtonStyle.red)
    view.add_item(button)
    await channel.send(view=view)

    async def button_callback(interaction):
        if head in interaction.user.roles:
            await channel.delete()
        else:
            await interaction.response.send_message("You cannot close the ticket!")
    button.callback = button_callback
  
@client.command()
async def close(ctx, ch_id: int):
    user = ctx.author
    head = get(user.guild.roles, id=957967793599418398)#head boys role
    if head in ctx.author.roles:
        channel = client.get_channel(ch_id)
        await channel.delete()
    else:
        await ctx.reply("You don't have the necessary perms to do so!")

@client.command()
async def modmail(ctx, reason:str, *, arg):
    try:
        user = ctx.author
        channel = client.get_channel(1004995434508460032)
        embed = nextcord.Embed(title="**MYTHS AND MAGIC**", description=f"This modmail was sent by \n{user.mention}|{user}|{user.id}", color=0x3498db)
        embed.add_field(name=f"**{reason}**", value=f"{arg}")
        embed.set_thumbnail(url = user.display_avatar)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed = embed)
        await ctx.reply("Your modmail has been successfully delivered!")
    except Exception as e:
        await ctx.reply("Your message could not be delivered\nPlease try again")
      
@client.command()
async def help(ctx):
    user = await client.fetch_user(1001338143003398237)
    embed = nextcord.Embed(title="**MYTHS AND MAGIC**", description=f"You can contact the staff in 2 ways. We are always ready to solve any problem or difficuly so feel free to express your problems", color=0x3498db)
    embed.add_field(name="**OPEN A TICKET**", value="*#ticket* :Creates a private channel between you and the staff where you can discuss your problems there with our staff. Once done the private channel gets deleted")
    embed.add_field(name="**OPEN A MODMAIL**", value="*#modmail [reason] [content]* :Dm this o the bot and  it sends your message to server staff and replies for the same!")
    embed.set_thumbnail(url = user.display_avatar)
    await ctx.reply(embed = embed)

client.run("******BOT-TOKEN******")
