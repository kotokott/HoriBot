import random
import discord
import os
import aiohttp
import asyncio
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from discord.ui import Modal, View, Button #, TextInput
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True  # Добавлено для работы с участниками
load_dotenv()
bot = commands.Bot(command_prefix = '/', intents=intents)


#---------------------------------------------
role_id = 1258410898968543312
WELCOME_CHANNEL_ID = 1258402199776792616
YOUR_CHANNEL_ID = 1272664648080031745
API_KEY = os.getenv('live_8x1Emr8VAL4imaTpNcWM2HPFBQG32fyvHOwXHIBBLv4bv8cUk8lWjK7Sm5aKbUEb')  # Убедитесь, что вы добавили CAT_API_KEY в .env файл
#---------------------------------------------

@bot.command(name="hori", description="Information about me^_^")
async def send_embed(ctx: discord.ApplicationContext):
    #await ctx.defer()
    # Создаем embed
    embed = discord.Embed(
        title="Hi! My name is Hori",
        description="and I help players on the Horizon server. I have various features that make some actions on the server easier. I am constantly updating and I have new features coming out. But if you notice any bug or error, you can create a ticket and write to my developers about it.",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Love to all, Hori💖")

    # Отправляем embed указанному пользователю
    await ctx.respond(embed=embed)



@bot.command(name="test", description="Please, test me(*^_^*)")
async def test(ctx: discord.ApplicationContext):
    await ctx.respond("Test completed!", ephemeral=True)

@bot.command(name="cat", description="Sends a random picture of a kitty🐈")
async def cat(ctx: discord.ApplicationContext):
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.thecatapi.com/v1/images/search?api_key={API_KEY}') as response:
            if response.status == 200:
                data = await response.json()
                cat_image_url = data[0]['url']
                await ctx.respond(cat_image_url)
            else:
                await ctx.respond("Couldn't get a picture of the kitty :(")



@bot.command(name="verify", description="Verification command")
@commands.has_permissions(administrator=True)
async def verify(ctx:commands.Context):
    await ctx.defer()
    message = await ctx.respond("Put the reaction ✅ for verification")
    await message.add_reaction('✅')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == '✅' and reaction.message.content == "Put the reaction ✅ for verification":
        guild = reaction.message.guild
        role = discord.utils.get(guild.roles, name="Verified")
        if role is None:
            role = await guild.create_role(name="Verified")
        member = guild.get_member(user.id)
        if member is not None:
            if role in member.roles:
                await user.send(f"{member.mention}, you're already verified")
            else:
                await member.add_roles(role)
                await user.send(f"{member.mention} Yay, you're verified. Now you can look around on the server😄")

@bot.event
async def on_ready():
    print("Sharky is running!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="at the kitties🐈"))

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name="Guest")
    if role is not None:
        await member.add_roles(role)
        print(f"Added role {role.name} to member {member.name}")
    else:
        print(f"Role 'Guest' not found on server {guild.name}")


class SurveyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Заявка для доступа к серверу")
        self.add_item(discord.ui.InputText(
            label="Твой ник в minecraft:",
            placeholder="Kotokott",
            min_length=4,
            max_length=20
        ))
        self.add_item(discord.ui.InputText(
            label="Твое имя:",
            placeholder="Даниил",
            min_length=3,
            max_length=20
        ))
        self.add_item(discord.ui.InputText(
            label="Твой возраст(только честно):",
            placeholder="16",
            min_length=1,
            max_length=2
        ))
        self.add_item(discord.ui.InputText(
            style=discord.InputTextStyle.long,
            label="Чем ты хочешь заниматься на сервере:",
            placeholder="Выживать и находить новых знакомых:3",
            min_length=20,
            max_length=300
        ))
        self.add_item(discord.ui.InputText(
            label="Насколько ты общительный(от 1 до 10):",
            placeholder="7",
            min_length=1,
            max_length=2
        ))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="**Новая заявка!**", color=discord.Color.purple())
        embed.add_field(name="**Ник в Minecraft:**", value=self.children[0].value, inline=False)
        embed.add_field(name="**Имя:**", value=self.children[1].value, inline=False)
        embed.add_field(name="**Возраст:**", value=self.children[2].value, inline=False)
        embed.add_field(name="**Занятия на сервере:**", value=self.children[3].value, inline=False)
        embed.add_field(name="**Общительность(от 1 до 10):**", value=self.children[4].value, inline=False)
        embed.set_footer(text="От Sharky🥰")
        channel = bot.get_channel(YOUR_CHANNEL_ID)  # Замените на ID вашего канала
        await channel.send(embed=embed)
        await interaction.response.send_message("Данные отправлены!", ephemeral=True)

#@bot.slash_command(name="survey", description="Отправить заявку для доступа к серверу")
#async def survey(ctx: discord.ApplicationContext):
    #modal = SurveyModal()
    #await ctx.send_modal(modal)

class MyView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @button(label="Заполнить заявку", style=discord.ButtonStyle.green, emoji="📋")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(SurveyModal())

@bot.command(name="form", description="Создать форму заявки для доступа к серверу")
@commands.has_permissions(administrator=True)
async def button_modal(ctx: discord.ApplicationContext):
    await ctx.respond("Заявка для получения доступа к серверу:3", view=MyView())

#@bot.command(name="create_ticket", description="Создайте тикет, если у вас возникла проблема!")
#@commands.has_permissions(manage_channels=True)
#async def openticket(ctx, member: discord.Member):
#    category = discord.utils.get(ctx.guild.categories, name="Тикеты")
#    await ctx.respond('Тикет открыт:3', ephemeral=True)
#    if not category:
#        category = await ctx.guild.create_category("Тикеты")
#
#   overwrites = {
#        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
#        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
#    }
#
#    channel = await ctx.guild.create_text_channel(f'тикет-{member.name}', category=category, overwrites=overwrites)
#    await channel.send(f'{member.mention}')
#    view = TicketButton()
#    await channel.send(f'Управление тикетом:', view=view)


#class TicketButton(discord.ui.View):
#    def __init__(self):
#        super().__init__(timeout=None)
#        self.role_id = '1258410847487787078'
#        # Добавляем кнопки
#        self.add_item(discord.ui.Button(label="Закрыть тикет", style=discord.ButtonStyle.red, emoji="❌"))
#        async def button_callback_1(self, button, interaction):
#            if "тикет-" in ctx.channel.name:
#                await ctx.channel.delete()
#        self.add_item(discord.ui.Button(label="Пинг модерации", style=discord.ButtonStyle.green, emoji="🔔"))
#        async def ping_role(self, button, interaction):
#            role = interaction.guild.get_role(self.role_id)
#            if role is None:
#                await interaction.response.send_message("Роль не найдена.", ephemeral=True)
#                return
#            await interaction.response.send_message(f"{role.mention} Вы были упомянуты!", allowed_mentions=discord.AllowedMentions(roles=True))
class TeamInvite(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Application to join the Horizon team:^")
        self.add_item(discord.ui.InputText(
            label="Your name:",
            placeholder="Jack",
            min_length=3,
            max_length=20
        ))
        self.add_item(discord.ui.InputText(
            label="Your age:",
            placeholder="16",
            min_length=1,
            max_length=2
        ))
        self.add_item(discord.ui.InputText(
            style=discord.InputTextStyle.long,
            label="What you can do:",
            placeholder="pixel-arts, models, plugin builds",
            min_length=20,
            max_length=300
        ))
        self.add_item(discord.ui.InputText(
            label="Your time zone:",
            placeholder="GMT +3",
            min_length=4,
            max_length=20
        ))
        self.add_item(discord.ui.InputText(
            label="How sociable you are(1 to 10):",
            placeholder="7",
            min_length=1,
            max_length=2
        ))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="**New application!**", color=discord.Color.purple())
        embed.add_field(name="**Name:**", value=self.children[0].value, inline=False)
        embed.add_field(name="**Age:**", value=self.children[1].value, inline=False)
        embed.add_field(name="**Skills:**", value=self.children[2].value, inline=False)
        embed.add_field(name="**Timezone:**", value=self.children[3].value, inline=False)
        embed.add_field(name="**Sociability(1 to 10):**", value=self.children[4].value, inline=False)
        embed.set_footer(text="From Hori🥰")
        channel = bot.get_channel(YOUR_CHANNEL_ID)  # Замените на ID вашего канала
        await channel.send(embed=embed)
        await interaction.response.send_message("The data has been sent! If you're a match, we'll email you:3", ephemeral=True)

class Team(View):
    def __init__(self):
        super().__init__(timeout=None)
    @button(label="Fill out an application", style=discord.ButtonStyle.green, emoji="📋")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(TeamInvite())

@bot.command(name="inviteteam", description="Create an application form for the Horizon team")
@commands.has_permissions(administrator=True)
async def button_modal(ctx: discord.ApplicationContext):
    await ctx.respond("Application to join the Horizon team:^", view=Team())

bot.run(os.getenv("TOKEN"))

