import discord
import asyncio
from datetime import datetime

TOKEN = '' #user token
WEBHOOK_URL = '' #webhook url for logs
TICKET_TOOL_ID = 557628352828014614 #ticket tool user id
CATEGORY_ID = 1083293648411701289 #category id to check
ROLE_ID = 1083293645928669187 #role id to give
VANITY_CODE = 'trustedopp' #vanity code
VANITY = f".gg/{VANITY_CODE}"
VANITY_WITH_STR = 'https://discord.gg/{0}'.format(VANITY_CODE)
VANITY_WITH_DD = '/{0}'.format(VANITY_CODE)
VANITY_WITH_DDD = 'discord.gg/{0}'.format(VANITY_CODE)

client = discord.Client()

def check_vanity(user:discord.Member):
    try:
        activity_name = user.activities[0].name
        if VANITY in activity_name or VANITY_WITH_STR in activity_name or VANITY_WITH_DD in activity_name or VANITY_WITH_DDD in activity_name:
            return True
    except:
        pass
    return False

def check_blacklist(user_id):
    with open('blacklist.txt', 'r') as f:
        blacklist = f.read().splitlines()
    if str(user_id) in blacklist:
        return True
    return False

async def add_to_blacklist(user_id):
    with open('blacklist.txt', 'a') as f:
        f.write(str(user_id) + '\n')

async def send_webhook_log(member:discord.Member,status:str):
    webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
    embed = discord.Embed(title=f"Newbie Role | {status}", description=f"{member.mention} has been {status} the newbie role.", color=00000)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User", value=f"{member.mention}|  ({member.id})", inline=False)
    embed.add_field(name="status", value=f"{status}", inline=False)
    await webhook.send(embed=embed)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.id == TICKET_TOOL_ID and message.channel.category_id == CATEGORY_ID:
        try:
            user_id = int(message.content.split(' ')[0].replace('<@','').replace('>',''))
            member = message.guild.get_member(user_id)
            if check_blacklist(user_id) == True:
                await message.channel.send(f"{member.mention} You are blacklisted.")
                return
            else:
                pass
            if check_vanity(member):
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                await message.channel.send(f"{current_time} | {member.mention} wait while we scan your profile.")
                await member.add_roles(discord.utils.get(message.guild.roles, id=ROLE_ID))
                role_tt = datetime.datetime.now().strftime("%H:%M:%S")
                await message.channel.send(f"{role_tt} | {member.mention} | {member.id} has been provided the newbie position.")
                await send_webhook_log(member, "added")
                await asyncio.sleep(10)
                await message.channel.send('$delete')
            else:
                await message.channel.send(f"{member.mention} You do not have vanity in your status.")
                await message.channel.send(f"{member.mention} Please add the vanity URL to your profile and Remake the ticket to fetch!.")
                await message.channel.send(f"{member.mention} The vanity URL is: {VANITY}")
                await send_webhook_log(member, "Failed to add")
                await asyncio.sleep(30)
                await message.channel.send('$delete')
        except Exception as e:
            print(e)
    elif message.content.startswith('!blacklist') and message.author.id == client.user.id:
        try:
            user_id = int(message.content.split(' ')[1].replace('<@', '').replace('>', '').replace('!', ''))
            member = message.guild.get_member(user_id)
            if member:
                with open('blacklist.txt', 'a') as f:
                    f.write(str(user_id) + '\n')
                await message.channel.send(f"{member.mention} has been added to the blacklist.")
            else:
                await message.channel.send("User not found.")
        except:
            await message.channel.send("Invalid syntax. Please use `!blacklist @user`.")
    
    elif message.content.startswith('!unblacklist') and message.author.id == client.user.id:
        try:
            user_id = int(message.content.split(' ')[1].replace('<@', '').replace('>', '').replace('!', ''))
            member = message.guild.get_member(user_id)
            if member:
                with open('blacklist.txt', 'r') as f:
                    blacklist = f.read().splitlines()
                if str(user_id) in blacklist:
                    #remove the line from txt file
                    with open('blacklist.txt', 'w') as f:
                        for line in blacklist:
                            if line != str(user_id):
                                f.write(line + '\n')
                    await message.channel.send(f"{member.mention} has been removed from the blacklist.")
                else:
                    await message.channel.send("User is not blacklisted.")
            else:
                await message.channel.send("User not found.")

        except:
            await message.channel.send("Invalid syntax. Please use `!unblacklist @user`.")
    
    else:
        pass


client.run(TOKEN)
