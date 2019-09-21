import discord
from discord.ext import commands
from discord.ext.commands import Bot,has_permissions
import json
import asyncio
point = open("tickets.txt").read()
channels = json.loads(point)
client = commands.Bot(command_prefix="-")
client.remove_command("help")
km = open("karma.txt").read()
karma = json.loads(km)
@client.event
async def on_ready():
    print("Yes I Am Ready")
    await client.change_presence(game=discord.Game(name="Message Me For Help",type=3))
@client.event
async def on_message(message):
    with open('tickets.txt', 'w') as file:
       file.write(json.dumps(channels))
    if message.content.startswith("-buy"):
        await client.process_commands(message)
    if message.author.bot or message.author == client.user:
        return
    if message.channel.is_private == True:
        if message.content.startswith("-buy") or message.content.startswith("-close"):
            return
        server = client.get_server('536486790975193089') #apka server id
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        user_perms = discord.PermissionOverwrite(read_messages=True)
        everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
        mine = discord.ChannelPermissions(target=message.author, overwrite=user_perms)
        if not message.author.id in channels:
            x = await client.create_channel(server, str(message.author), everyone)
            channels[message.author.id] = x.id
            await client.send_message(message.channel,"**Ticket Created SuccesFully, Our Staff Will be With you soon** \n __*First Try to Explain your Problem*__")
        else:
            channel = discord.utils.get(server.channels,id=str(channels[message.author.id]))
            await client.send_message(channel,str(message.content)+" By "+"<@"+str((message.author.id))+">")
            if len(message.attachments)!=0:
                await client.send_message(channel,message.attachments[0]["url"])
    else:
        for i,j in channels.items():
            us = None
            if message.channel.id == j:
                print("Hi")
                det = (*channels,)
                for i in det:
                    if channels[i] == message.channel.id:
                        us = i
                server = client.get_server('536486790975193089')
                if not us in channels:
                    await client.say("No user found with this Ticket")
                elif channels[us] != message.channel.id:
                    await client.say("This user is not belongs to this Ticket")
                else:
                    usn = message.server.get_member(us)
                    if message.content == "close" or message.content == "Close" or message.content.lower() == "close" :
                        x = message.content
                        y = x.find("e" )
                        z = x[y+1:]
                        if z== " ":
                            z = "No Reason"
                        del channels[usn.id]
                        await client.delete_channel(message.channel)
                        await client.send_message(usn,"Your Ticket has Been Closed Due to Reason %s \n "%z)
                        return None
                    else:
                        await client.send_message(usn, str(message.author)+" " + str(message.content))
                        await client.send_message(message.channel,"Message has been sent")
        

        
    await client.process_commands(message)
@client.command(pass_context=True,no_pm=True)
@has_permissions(manage_roles=True, ban_members=True)
async def kick(ctx,user:discord.User):
    if ctx.message.author.server_permissions.kick_members:
        if user.id != ctx.message.author.id:
            if not user.server_permissions.kick_members:
                x = ctx.message.content.find(" ")
                y = ctx.message.content.find(" ",x)
                await client.kick(user)
                await client.say("User Has been Kicked off")
            else:
                await client.say("I can't Kick Him")
        else:
            await client.say("Self Kick is Not enabled")
    else:
        await client.say("You Dont have permissions")

@client.command(pass_context=True,no_pm=True)
async def ban(ctx,user:discord.User):
    if ctx.message.author.server_permissions.ban_members:
        if user.id != ctx.message.author.id:
            if not user.server_permissions.ban_members:
                await client.ban(user,7)
                await client.say("User Has been Banned")
            else:
                await client.say("I can't Ban Him")
        else:
            await client.say("Self Ban is Not enabled")
    else:
        await client.say("You Dont have permissions")

@client.command(pass_context=True,no_pm=True)
async def role(ctx,user:discord.User,role:discord.Role):
    if ctx.message.author.server_permissions.manage_roles:
        if role not in user.roles:
            await client.add_roles(user,role)
            await client.say('Roles has been added')
        elif role in user.roles:
            await client.remove_roles(user,role)
            await client.say("Role has been Removed")
@role.error
async def role_error(error,ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, "**Missing Permissions to add that Role** " )
    if isinstance(error, commands.BadArgument):
        await client.send_message(ctx.message.channel, "**Please Check the role that you have given** " )

@client.command(pass_context=True,no_pm=True)
async def say(ctx):
    me = ctx.message.content.find(" ")
    x = ctx.message.content[me:]
    await client.delete_message(ctx.message)
    await client.say(x)
@client.command(pass_context=True,no_pm=True)
async def sweep(ctx,number:int):
    x =[]
    c=0
    async for msgs in client.logs_from(ctx.message.channel,limit=number):
        c+=1
        await client.delete_message(msgs)
    x = await client.say(str(c)+" messages has been deleted by %s"%ctx.message.author)
    asyncio.sleep(5)
    await client.delete_message(x)

@client.command(pass_context=True,no_pm=True)
async def warn(ctx,user:discord.User,*, reason):
    await client.delete_message(ctx.message)
    await client.say(str(user.mention)+" **has been Warned because of** ```%s```"%reason)
@client.command(pass_context=True,no_pm=True)
async def help(ctx):
    em = discord.Embed(title="Help",description="Shows This Message",colour=discord.Colour.dark_orange())
    em.add_field(name="Kick" ,value="Usage kick -kick <member>",inline=False)
    em.add_field(name="Ban" ,value="Usage Ban -ban <member>",inline=False)
    em.add_field(name="Role" ,value="Usage Role -role <member> <role>",inline=False)
    em.add_field(name="Warn", value="Usage Wanr -warn <member> <reason>",inline=False)
    em.add_field(name="Say" ,value="Usage say -say <Message You Want to Say>",inline=False)
    em.add_field(name="Sweep", value="Usage Sweep -sweep  <number of Message>",inline=False)
    em.set_footer(text="Requested By %s"%ctx.message.author)
    em.set_thumbnail(url=ctx.message.author.avatar_url)
    em.set_author(name=client.user.name,icon_url=client.user.avatar_url)
    await client.say(embed=em)

@client.command(pass_context=True,no_pm=True)
async def mute(ctx,user:discord.User):
    role = discord.utils.get(ctx.message.server.roles,name="muted")
    if not role:
        perms = discord.Permissions(send_messages=False,read_messages=False)
        await client.create_role(ctx.message.server,name="muted",permissions=perms)
    role = discord.utils.get(ctx.message.server.roles,name="muted")
    if role not in user.roles:
        print(role.id)
        await client.add_roles(user,role)
        await client.say("User has been muted")
    else:
        await client.say("He is already a muted one and I am unmuting him")
        await client.remove_roles(user,role)
msgc = []
global bc,gc
bc = 0
gc =0
msc = []
@client.event
async def on_reaction_add(reaction,user):
    global bc,gc
    count = False
    reactmsg = reaction.message
    if reaction.emoji == "🔼":
        bc+=1
        if reaction.count >= 5:
            print(msgc)
            if user.id not in msgc and reaction.message.id not in msc:
                msgc.append(user.id)
                msc.append(reaction.message.id)
                if reaction.message.author.id not in karma:
                    await client.send_message(reaction.message.channel,"Please our Karma Terms by -agree")
                    return
                else:
                    karma[reaction.message.author.id] +=5
                    with open("karma.txt","w") as f:
                        f.write(json.dumps(karma))
                    await client.send_message(reaction.message.channel,"User has been set +1 Karma")
    
                    bc = 0
                    asyncio.sleep(20)
                    msgc.remove(user.id)
            else:
                return None
                
    elif reaction.emoji == "🔽":
        gc+=1
        if reaction.count >=1:
            if user.id not in msgc and reaction.message.id not in msc:
                msgc.append(user.id)
                print(msgc)
                msc.append(reaction.message.id)
                
                if reaction.message.author.id not in karma:
                    await client.send_message(reaction.message.channel,"Please our Karma Terms by -agree")
                    return
                else:
                    karma[reaction.message.author.id] -=5
                    with open("karma.txt","w") as f:
                        f.write(json.dumps(karma))
                    await client.send_message(reaction.message.channel,"User has been set -5 Karma")
                    asyncio.sleep(20)
                    msgc.remove(str(user.id))
            else:
                return None
                
                

    
@client.command(pass_context=True,no_pm=True)
async def agree(ctx):
    karma[ctx.message.author.id] = 0
    with open("karma.txt","w") as f:
                    f.write(json.dumps(karma))
    await client.say("You have agreed Karma with 0")
    print(karma)
@client.command(pass_context=True,no_pm=True)
async def mk(ctx):
    if ctx.message.author.id in karma:
        await client.say("You have %s of Karma points"%karma[ctx.message.author.id])
        await client.add_reaction(ctx.message,emoji="🔼")
    else:
        await client.say("Not in our list")
    
client.run("NTM2NTg4NjcwMzIxNDI2NDUz.DyY5qQ.ClQkKzxsiNUGpj5uudUJjy3Suqg")



