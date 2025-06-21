import random
import discord
import os
import aiohttp
import asyncio

from discord import default_permissions, guild
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from discord.ui import Modal, InputText, View, Button
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True  # Добавлено для работы с участниками
load_dotenv()
bot = discord.Bot(intents=intents)


#---------------------------------------------
role_id = 1274773142723891294
WELCOME_CHANNEL_ID = 1274771798721826897
API_KEY = os.getenv('live_8x1Emr8VAL4imaTpNcWM2HPFBQG32fyvHOwXHIBBLv4bv8cUk8lWjK7Sm5aKbUEb')  # Убедитесь, что вы добавили CAT_API_KEY в .env файл
#---------------------------------------------

@bot.command(name="hori", description="Information about me^_^")
async def send_embed(ctx: discord.ApplicationContext):
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



verification_message_id = None

@bot.command(name="verify", description="Verification command")
@default_permissions(administrator=True)
async def verify(ctx: discord.ApplicationContext):
    global verification_message_id
    response = await ctx.respond("Put the reaction ✅ for verification")
    message = await response.original_response()
    await message.add_reaction('✅')
    verification_message_id = message.id # Сохраняем ID

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    # Проверяем по ID сообщения, а не по тексту
    if reaction.message.id == verification_message_id and reaction.emoji == '✅':
        guild = reaction.message.guild
        # Ищем роль по имени. Лучше использовать ID роли для надежности.
        role = discord.utils.get(guild.roles, name="Verified")
        if role is None:
            # Если роли нет, можно создать ее (требуются права у бота)
            await user.send("Verification role not found on the server.")
            return

        member = guild.get_member(user.id)
        if member is not None:
            if role in member.roles:
                await user.send(f"{member.mention}, you're already verified")
            else:
                await member.add_roles(role)
                await user.send(f"{member.mention} Yay, you're verified. Now you can look around on the server^_^")

@bot.event
async def on_ready():
    print("Hori is running!")
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


'''class SurveyModal(discord.ui.Modal):
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
    @discord.ui.button(label="Заполнить заявку", style=discord.ButtonStyle.green, emoji="📋")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(SurveyModal())

@bot.command(name="form", description="Создать форму заявки для доступа к серверу")
@commands.has_permissions(administrator=True)
async def button_modal(ctx: discord.ApplicationContext):
    await ctx.respond("Заявка для получения доступа к серверу:3", view=MyView())'''

@bot.command(name="createticket", description="If you have any problems, please create a ticket!")
#@default_permissions(manage_channels=True)
async def openticket(ctx, member: discord.Member):
    category = discord.utils.get(ctx.guild.categories, name="Tickets")
    await ctx.respond('ticket created:3', ephemeral=True)
    if not category:
        category = await ctx.guild.create_category("Tickets")

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    channel = await ctx.guild.create_text_channel(f'ticket-{member.name}', category=category, overwrites=overwrites)
    await channel.send(f'{member.mention}')
    view = TicketButton()
    await channel.send(f'Ticket management:', view=view)


class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Кнопки не исчезнут со временем
        self.moderator_role_id = 1274761910130315277  # Лучше использовать int, но str тоже работает

    @discord.ui.button(label="Close ticket", style=discord.ButtonStyle.red, emoji="❌", custom_id="close_ticket")
    async def close_ticket_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # `interaction` — это взаимодействие, которое происходит при нажатии кнопки.
        # Из него мы можем получить канал, пользователя и т.д.
        # `ctx` здесь недоступен.

        # Простая проверка, что канал действительно является тикетом
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("The ticket will be closed in 5 seconds...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("This is not a ticket channel", ephemeral=True)

    @discord.ui.button(label="Ping moderators", style=discord.ButtonStyle.green, emoji="🔔", custom_id="ping_moderators")
    async def ping_moderators_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Получаем роль из гильдии, где произошло взаимодействие
        role = interaction.guild.get_role(self.moderator_role_id)

        if role is None:
            await interaction.response.send_message("Moderation role not found", ephemeral=True)
            return

        # Отправляем пинг в этот же канал и подтверждаем действие
        await interaction.response.send_message("Moderation has been called!", ephemeral=True)
        await interaction.channel.send(f"{role.mention}, You have been called for help in a ticket!")



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
            placeholder="pixel-arts, models, code",
            min_length=20,
            max_length=300
        ))
        self.add_item(discord.ui.InputText(
            label="Where are you from(timezone):",
            placeholder="Australia | UTC +1",
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
        member = interaction.user
        role = discord.utils.get(interaction.guild.roles, name="Applicant")
        if role:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                print("Error(role)")
        else:
            print("role not found")

        embed = discord.Embed(title="**New application!**", color=discord.Color.purple())
        embed.add_field(name="**Name:**", value=self.children[0].value, inline=False)
        embed.add_field(name="**Age:**", value=self.children[1].value, inline=False)
        embed.add_field(name="**Skills:**", value=self.children[2].value, inline=False)
        embed.add_field(name="**Timezone:**", value=self.children[3].value, inline=False)
        embed.add_field(name="**Sociability(1 to 10):**", value=self.children[4].value, inline=False)
        embed.set_footer(text="From Hori🥰")
        channel = bot.get_channel(1328453129158656000)  # Замените на ID вашего канала
        await channel.send(embed=embed)
        await interaction.response.send_message("Data sent! If you match, we will write to you:3", ephemeral=True)
        await interaction.followup.send(f"You have been given a role {role.name}", ephemeral=True)


class Team(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fill out an application", style=discord.ButtonStyle.green, emoji="📋")
    async def application_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(TeamInvite())

@bot.command(name="inviteteam", description="Create an application form for the Horizon team")
@default_permissions(administrator=True)
async def button_modal(ctx: discord.ApplicationContext):
    await ctx.respond("Application to join the Horizon team:^", view=Team())

bot.run(os.getenv("TOKEN"))

