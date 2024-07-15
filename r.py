import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

WELCOME_CHANNEL_ID = '1262382072996171868'  # Replace with your welcome channel ID
WELCOME_MESSAGE_ID = '1262401150272147600'
ROLE_EMOJIS = {
    '👍': '1262395200655855698',  # Replace with your role ID and corresponding emoji
    '👎': '1262395622233997395',
    # Add more emoji-role pairs as needed
}

def set_globvar(aa):
    global WELCOME_MESSAGE_ID    # Needed to modify global copy of globvar
    WELCOME_MESSAGE_ID = aa

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
    if channel:
        welcome_message = await channel.send(
            f"Welcome {member.mention}! Please react to this message to get your role.\n"
            "👍 for Role 1\n"
            "👎 for Role 2"
            # Add more options as needed
        )
        set_globvar(welcome_message.id)

        for emoji in ROLE_EMOJIS.keys():
            await welcome_message.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != WELCOME_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    role_id = ROLE_EMOJIS.get(str(payload.emoji))
    if role_id:
        role = guild.get_role(int(role_id))
        if role:
            await member.add_roles(role)
            print(f"Assigned {role.name} to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != WELCOME_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    role_id = ROLE_EMOJIS.get(str(payload.emoji))
    if role_id:
        role = guild.get_role(int(role_id))
        if role:
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.name}")

bot.run('BOT-TOKEN')