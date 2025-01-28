# imports
import os
import time
from typing import Final

import re
import lavarand
import discord
import gspread
from discord import ui
from discord.ext import commands
from dotenv import load_dotenv
from google.oauth2.service_account import (Credentials)



from gspread.exceptions import APIError

import responses

# API creds
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("Creds.json", scopes=scopes)
client = gspread.authorize(creds)

# Specify sheets
sheet_id = "1Tt6GCm9_9gG0k-0IPVBcW7WCLzVfA7t-AxqJGFqI0_M"
workbook1 = client.open_by_key(sheet_id)
sheet_id2 = "1espNxTCzMOwAYnQyEnHjJmDT9aOTf6JtDfiY0mrqtFU"
workbook2 = client.open_by_key(sheet_id2)

# Specify worksheets
sheet = workbook1.get_worksheet(0)
vtaData = workbook1.get_worksheet(1)
vpdData = workbook1.get_worksheet(2)
vggData = workbook1.get_worksheet(3)
vauData = workbook1.get_worksheet(4)
deptruData = workbook1.get_worksheet(5)
testData = workbook1.get_worksheet(6)
SensData = workbook2.get_worksheet(0)

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="/commands"), status=discord.Status.offline)

global preFix
preFix = "/"


async def remove_non_digits(string):
    return re.sub(r'\D', '', string)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is online")


# @bot.tree.command(name='sync', description='Developer only')
# async def sync(interaction: discord.Interaction):
#     await bot.tree.sync()
#     print('Command tree synced.')
#     await interaction.response.send_message(content="Worked")


@bot.tree.command(name="credits", description="Displays the bot credits.")
async def botCreds(interaction: discord.Interaction):
    number = await remove_non_digits(lavarand.random())
    creditEmbed = discord.Embed(title="Credits", color=discord.Color.Cirilla_green())
    creditEmbed.add_field(name="Developer(s)", value="```Cirilla_dev```", inline=False)
    creditEmbed.add_field(name="Coding helper(s)", value="```Cynthia Vlalence\nMyWholeLifeIsA1ie```", inline=False)
    if number[0] == 1:
        creditEmbed.add_field(name="Scum of the earth", value="```MyWholeLifeIsA1ie```", inline=False)
    else:
        creditEmbed.add_field(name="Head tester(s)", value="```MyWholeLifeIsA1ie```", inline=False)
    creditEmbed.add_field(name="Tester(s)", value="```MyWholeLifeIsA1ie\nIIranzay\nBobbbobobjg\nHamzoAlpennau\nSpiffy_Stars```", inline=False)
    creditEmbed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')
    await interaction.response.send_message(embed=creditEmbed)


# noinspection PyUnresolvedReferences
@bot.tree.command(name="commands", description="Get a list of the commands OL bot uses")
async def commands(interaction: discord.Interaction):
    aCheckID = str(interaction.user.id)
    if True not in responses.ctxauthCheck(aCheckID):
        await interaction.response.send_message("```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        help_embed = discord.Embed(title='Commands list', color=discord.Color.Cirilla_green())
        help_embed.add_field(name=f'{preFix}commands', value='```Get command list```', inline=False)
        help_embed.add_field(name=f'{preFix}announce (message)', value='```Allows a message to be announced to sList channels.```', inline=False)
        help_embed.add_field(name=f'{preFix}authCheck (ID)', value='```Checks the authority levels for the given discord ID```', inline=False)
        help_embed.add_field(name=f'{preFix}authorize (ID) (Level)', value='```Allows level 3 operators to assign level 1 or level 2 authority```', inline=False)
        help_embed.add_field(name=f'{preFix}credits', value='```Displays the bot credits.```', inline=False)
        help_embed.add_field(name=f'{preFix}end', value='```Allows level 2 or 3 operators to take the bot offline```', inline=False)
        help_embed.add_field(name=f'{preFix}file', value='```Opens a Modal to allow automatic logging of punishments```')
        help_embed.add_field(name=f'{preFix}get (Username)', value='```Get a User\'s logged punishments```', inline=False)
        help_embed.add_field(name=f'{preFix}help', value='```Get discord\'s automatic bot commands list```', inline=False)
        help_embed.add_field(name=f'{preFix}issue', value='```Mark the previous interaction for review```', inline=False)
        help_embed.add_field(name=f'{preFix}ping', value='```Return\'s bot\'s discord.py and gSpread API delay per request```', inline=False)
        help_embed.add_field(name=f'{preFix}unauthorize (ID) (Level)', value='```Allows level 3 or 2 operators to unassign authority one level below theirs```', inline=False)
        help_embed.add_field(name=f'{preFix}unannounce', value='```Removes the last announcement```', inline=False)
        help_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')
        await interaction.response.send_message(embed=help_embed)


async def log(interaction: discord.Interaction):
    # Logging the user action
    print(f'{interaction.user.name} ran the {interaction.command.name} command at {interaction.created_at}')

    # Construct the log entry
    fullLogs = str(SensData.cell(7, 2).value) + " " + str(f'{interaction.user.name} ran the log command at {interaction.created_at}')

    # Update the Google Sheet with the log entry
    SensData.update_acell('B7', fullLogs)


@bot.tree.command(name="get", description="Get a person's logged punishments")
async def get(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    await log(interaction)
    # Check if the user is authorized
    aCheckID = str(interaction.user.id)
    try:
        if username == "Vaktus":
            await interaction.followup.send(content="```ansi\n[0;31mERROR OO - [CLASSIFIED].[0;0m```")
        else:
            if True not in responses.ctxauthCheck(aCheckID):
                await interaction.followup.send(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
            else:

                # try:
                # Get the subject from the interaction's options (assuming it's a string parameter)
                subject = username
                VTA = await infoGet2(subject, vtaData)
                VPD = await infoGet2(subject, vpdData)
                VGG = await infoGet2(subject, vggData)
                VAU = await infoGet2(subject, vauData)
                DEPTRU = await infoGet2(subject, deptruData)
                ems = []

                if not VTA and not VPD and not VGG and not VAU and not DEPTRU:
                    await interaction.followup.send(content="```ansi\n[0;31mERROR 2 - Subject not found in searched range.[0;0m```")
                else:
                    # Create embeds for each organization data and send them

                    if VTA:
                        while len(VTA) > 0:
                            VTAembed = discord.Embed(color=discord.Color.VTACyan())
                            VTAembed.add_field(name="Organization:", value="```ansi\n[0;36mVyyrahk Teacher's Association[0;0m```", inline=False)
                            VTAembed.add_field(name="Name:", value=f'```{VTA[0]}```', inline=False)
                            del VTA[0]
                            VTAembed.add_field(name="Entry number:", value=f'```{VTA[0]}```', inline=False)
                            del VTA[0]
                            VTAembed.add_field(name="Action:", value=f'```{VTA[0]}```', inline=False)
                            del VTA[0]
                            VTAembed.add_field(name="Description:", value=f'```{VTA[0]}```', inline=False)
                            del VTA[0]

                            try:
                                if "http" in VTA[0]:

                                    VTAembed.add_field(name="Evidence:", value=f'```{VTA[0]}```', inline=False)
                                else:
                                    VTAembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)


                            except IndexError:
                                VTAembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                            ems.append(VTAembed)

                    if VPD:
                        while len(VPD) > 0:
                            VPDembed = discord.Embed(color=discord.Color.VPDBlue())
                            VPDembed.add_field(name="Organization:", value="```ansi\n[0;34mVyyrahk Police Department[0;0m```", inline=False)
                            VPDembed.add_field(name="Name:", value=f'```{VPD[0]}```', inline=False)
                            del VPD[0]
                            VPDembed.add_field(name="Entry number:", value=f'```{VPD[0]}```', inline=False)
                            del VPD[0]
                            VPDembed.add_field(name="Action:", value=f'```{VPD[0]}```', inline=False)
                            del VPD[0]
                            VPDembed.add_field(name="Description:", value=f'```{VPD[0]}```', inline=False)
                            del VPD[0]

                            try:
                                if "http" in VPD[0]:

                                    VPDembed.add_field(name="Evidence:", value=f'```{VPD[0]}```', inline=False)
                                else:
                                    VPDembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)


                            except IndexError:
                                VPDembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                            ems.append(VPDembed)

                    if VGG:
                        while len(VGG) > 0:
                            VGGembed = discord.Embed(color=discord.Color.VGGBlack())
                            VGGembed.add_field(name="Organization:", value="```ansi\n[0;30mVyyrahk Gladiators Guild[0;0m```", inline=False)
                            VGGembed.add_field(name="Name:", value=f'```{VGG[0]}```', inline=False)
                            del VGG[0]
                            VGGembed.add_field(name="Entry number:", value=f'```{VGG[0]}```', inline=False)
                            del VGG[0]
                            VGGembed.add_field(name="Action:", value=f'```{VGG[0]}```', inline=False)
                            del VGG[0]
                            VGGembed.add_field(name="Description:", value=f'```{VGG[0]}```', inline=False)
                            del VGG[0]

                            try:
                                if "http" in VGG[0]:

                                    VGGembed.add_field(name="Evidence:", value=f'```{VGG[0]}```', inline=False)
                                else:
                                    VGGembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)


                            except IndexError:
                                VGGembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                            ems.append(VGGembed)

                    if VAU:
                        while len(VAU) > 0:
                            VAUembed = discord.Embed(color=discord.Color.VAUPurple())
                            VAUembed.add_field(name="Organization:", value="```ansi\n[0;35mVyyrahk Actors Union[0;0m```", inline=False)
                            VAUembed.add_field(name="Name:", value=f'```{VAU[0]}```', inline=False)
                            del VAU[0]
                            VAUembed.add_field(name="Entry number:", value=f'```{VAU[0]}```', inline=False)
                            del VAU[0]
                            VAUembed.add_field(name="Action:", value=f'```{VAU[0]}```', inline=False)
                            del VAU[0]
                            VAUembed.add_field(name="Description:", value=f'```{VAU[0]}```', inline=False)
                            del VAU[0]

                            try:
                                if "http" in VAU[0]:

                                    VAUembed.add_field(name="Evidence:", value=f'```{VAU[0]}```', inline=False)
                                else:
                                    VAUembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)


                            except IndexError:
                                VAUembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                            ems.append(VAUembed)

                        if DEPTRU:
                            while len(DEPTRU) > 0:
                                DEPTRUembed = discord.Embed(color=discord.Color.DEPTRUYellow())
                                DEPTRUembed.add_field(name="Organization:", value="```ansi\n[0;33mDepartment of Truth[0;0m```", inline=False)
                                DEPTRUembed.add_field(name="Name:", value=f'```{DEPTRU[0]}```', inline=False)
                                del DEPTRU[0]
                                DEPTRUembed.add_field(name="Entry number:", value=f'```{DEPTRU[0]}```', inline=False)
                                del DEPTRU[0]
                                DEPTRUembed.add_field(name="Action:", value=f'```{DEPTRU[0]}```', inline=False)
                                del DEPTRU[0]
                                DEPTRUembed.add_field(name="Description:", value=f'```{DEPTRU[0]}```', inline=False)
                                del DEPTRU[0]

                                try:
                                    if "http" in DEPTRU[0]:

                                        DEPTRUembed.add_field(name="Evidence:", value=f'```{DEPTRU[0]}```', inline=False)
                                    else:
                                        DEPTRUembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                                except IndexError:
                                    DEPTRUembed.add_field(name="Evidence:", value="```ansi\n[0;31mNo evidence link provided by Organization[0;0m```", inline=False)
                                ems.append(DEPTRUembed)
                    if ems:
                        await interaction.followup.send(embeds=ems)
                    else:
                        await interaction.followup.send(content="```ansi\n[0;31mERROR 2 - Subject not found in searched range.[0;0m```")
    except APIError:
        await interaction.followup.send('```ansi\n[0;31mAPIERROR 429 - Read requests per minute per user failed, try again soon.[0;0m```')
    # except:
    #     await interaction.followup.send(content="```ansi\n[0;31mAn exception has occured!\n\nThis is likely caused by too many API requests in a minute. If this continues after waiting, contact Cirilla_dev.[0;0m```")


@bot.tree.command(name="authcheck", description="Return a list of user's authority levels")
async def authCheck(interaction: discord.Interaction, discord_id: str):
    # Log the interaction (passing the interaction object to the log function)
    await log(interaction)
    await interaction.response.defer()

    aCheckID = str(interaction.user.id)
    if True not in responses.ctxauthCheck(aCheckID):
        await interaction.followup.send(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        subject = discord_id
        authCheck_embed = discord.Embed(title=f"Authority level check for {subject}", color=discord.Color.Cirilla_green())
        authCheck_embed.add_field(name="Level 3: ", value=f"```{responses.ctxauthCheck(subject)[0]}```")
        authCheck_embed.add_field(name="Level 2: ", value=f"```{responses.ctxauthCheck(subject)[1]}```")
        authCheck_embed.add_field(name="Level 1: ", value=f"```{responses.ctxauthCheck(subject)[2]}```")
        authCheck_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')
        await interaction.followup.send(embed=authCheck_embed)


@bot.tree.command(name="ping", description="Get the discord API and gSpread API latency per request in ms")
async def ping(interaction: discord.Interaction):
    # Log the interaction
    await log(interaction)

    aCheckID = str(interaction.user.id)
    if True not in responses.ctxauthCheck(aCheckID):
        await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        start_time = time.time()
        SensData.find("705669396999176233")
        end_time = time.time()
        glatency = end_time - start_time

        # Ping embed for bot's latency
        ping_embed = discord.Embed(title="Ping", description="Latency in ms", color=discord.Color.Cirilla_green())
        ping_embed.add_field(name=f"{bot.user.name}'s Latency (ms): ", value=f"```{round(bot.latency * 1000)}ms```", inline=False)
        ping_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')

        # Ping embed for Google Sheets API latency
        gping_embed = discord.Embed(title="GSpread ping", description="Latency in ms", color=discord.Color.Cirilla_green())
        gping_embed.add_field(name=f"Google Sheets API's Latency per request (ms): ", value=f"```{round(glatency * 1000)}ms```", inline=False)
        gping_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')

        # Send the embed responses
        await interaction.response.send_message(embed=ping_embed)
        await interaction.followup.send(embed=gping_embed)


@bot.tree.command(name="end", description="For authority level 2 and above, turns the bot off.")
async def end(interaction: discord.Interaction):
    # Log the interaction
    await log(interaction)

    subject = str(interaction.user.id)
    if responses.ctxauthCheck(subject)[1] or responses.ctxauthCheck(subject)[0]:
        print(f'{interaction.user.name} successfully ran the /end command at {interaction.created_at}')
        await interaction.response.send_message(content="```ansi\n[0;37m Bot successfully turned off.[0;0m```")
        await bot.close()
    else:
        print(f'{interaction.user.name} attempted to use the /end command at {interaction.created_at}')
        await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")


@bot.tree.command(name="issue", description="Marks the previous interaction for developer review")
async def issue(interaction: discord.Interaction):
    # Log the interaction
    await log(interaction)

    aCheckID = str(interaction.user.id)
    if True not in responses.ctxauthCheck(aCheckID):
        await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        print(f'{interaction.user.name} marked the previous interaction for review. {interaction.created_at}')
        await interaction.response.send_message(content="```ansi\n[0;37m Interaction successfully reported.[0;0m```")


@bot.tree.command(name="unauthorize", description="Unauthorize someone at a specific authority level")
async def unauthorize(interaction: discord.Interaction, discord_id: str, auth_level: int):
    author = str(interaction.user.id)
    # Extract subject and level from the interaction command arguments
    try:
        subject = discord_id  # Adjust if needed depending on argument passing style
        level = auth_level
    except IndexError:
        await interaction.response.send_message(content="Invalid parameters provided.", ephemeral=True)
        return

    list3 = str(SensData.cell(level, 2).value)
    list2 = list3.replace(subject, "")

    unauth_embed = discord.Embed(color=discord.Color.Cirilla_green())
    unauth_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')

    # Check for authorization level
    if responses.ctxauthCheck(author)[0]:
        if level == 3:
            temp = "```ansi\n[0;31mERROR 7 - Only Cirilla_dev may remove admins. Use '.end' to shut down the bot in-cases of AA. [0;0m```"
        else:
            if subject in SensData.cell(level, 2).value:
                temp = f"```ansi\n[0;37mSuccessfully removed {subject} from level {level}[0;0m```"
                await log(interaction)  # Log the action
                SensData.update_cell(level, 2, list2)
            else:
                temp = "```ansi\n[0;31mERROR 2 - ID not found at specified level[0;0m```"
    else:
        temp = "```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```"
        await log(interaction)  # Log the action for unauthorized access

    unauth_embed.add_field(name=f"Attempt to unauthorize: {subject} at level {level}", value=f"{temp}", inline=False)
    await interaction.response.send_message(embed=unauth_embed)


# @bot.tree.command(name="colortest", description="For developers to test colors on different embeds")
# async def colortest(interaction: discord.Interaction, color: str):
#     # Extract the author and check authorization level
#     author_id = str(interaction.user.id)
#     if not responses.ctxauthCheck(author_id)[0]:
#         await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
#         return
#
#     # Extract color argument from the interaction
#     try:
#         color_arg = color  # Assuming 'color' is the first argument
#     except IndexError:
#         await interaction.response.send_message(content="Invalid color specified. Please choose from 'purple', 'blue', or 'green'.", ephemeral=True)
#         return
#
#     # Create color_embed based on the color argument
#     if color_arg == 'purple':
#         color_embed = discord.Embed(color=discord.Color.Cirilla_purple())
#     elif color_arg == 'blue':
#         color_embed = discord.Embed(color=discord.Color.Cirilla_blue())
#     elif color_arg == 'green':
#         color_embed = discord.Embed(color=discord.Color.Cirilla_green())
#     else:
#         await interaction.response.send_message(content="Invalid color specified. Please choose from 'purple', 'blue', or 'green'.", ephemeral=True)
#         return
#
#     # Add fields to the embed
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.add_field(name="TESTING", value="TESTING TESTING TESTING TESTING TESTING TESTING TESTING ")
#     color_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')
#
#     # Send the embed
#     await interaction.response.send_message(embed=color_embed)


@bot.tree.command(name="authorize", description="Authorize someone at a specific authority level")
async def authorize(interaction: discord.Interaction, discord_id: str, auth_level: int):
    # Extract the author (interacting user) and check if they are authorized
    author_id = str(interaction.user.id)

    # Ensure the interaction includes the required arguments
    try:
        subject_id = str(discord_id)  # ID of the subject to authorize
        level = auth_level  # Level of authority to assign
        fullList = str(SensData.cell(level, 2).value)
        success = False
    except IndexError:
        await interaction.response.send_message(content="Missing arguments. Usage: /authorize <subject_id> <level>", ephemeral=True)
        return

    # Prepare embed for feedback
    auth_embed = discord.Embed(color=discord.Color.Cirilla_green())
    auth_embed.set_footer(text="OL Bot made and maintained by Cirilla_dev", icon_url='https://cdn.discordapp.com/avatars/705669396999176233/078ebc55ea389bc93762349b06fe73a0.png?size=1024')

    # Check if the author is authorized
    if responses.ctxauthCheck(author_id)[0]:  # Admin check
        if level == 3 and author_id != "705669396999176233":
            temp = "```ansi\n[0;31mERROR 4 - You may only assign authority to those below you.[0;0m```"
            success = False
        else:
            if subject_id not in str(SensData.cell(level, 2).value):
                temp = f"```ansi\n[0;37mSuccessfully given {subject_id} level {level} authority.[0;0m```"
                await log(interaction)
                SensData.update_cell(level, 2, fullList + " " + subject_id)
                success = True
            else:
                temp = f"```ansi\n[0;37mID:{subject_id} already has level {level} authority.[0;0m```"
                success = False
    elif responses.ctxauthCheck(author_id)[1]:  # Moderator check
        if level == 2:
            temp = "```ansi\n[0;31mERROR 4 - You may only assign authority to those below you.[0;0m```"
            success = False
        else:
            if subject_id not in SensData.cell(level, 2).value:
                temp = f"```ansi\n[0;37mSuccessfully given {subject_id} level {level} authority.[0;0m```"
                await log(interaction)
                SensData.update_cell(level, 2, fullList + " " + subject_id)
                success = True
            else:
                temp = f"```ansi\n[0;37mID:{subject_id} already has level {level} authority.[0;0m```"
                success = False
    else:
        temp = "```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```"
        await log(interaction)
        success = False

    # Add the status message to the embed and send it
    if success:
        auth_embed.add_field(name=f"Success:", value=f"```ansi\n[0;32m{success}[0;0m```", inline=False)
    elif not success:
        auth_embed.add_field(name=f"Success:", value=f"```ansi\n[0;31m{success}[0;0m```", inline=False)
        auth_embed.add_field(name=f"Reason for failure", value=f"{temp}", inline=False)
    auth_embed.add_field(name="Subject ID:", value=f"```{subject_id}```")
    auth_embed.add_field(name="Authority Level:", value=f"```{level}```")
    await interaction.response.send_message(embed=auth_embed)


@bot.tree.command(name="announce", description="Announces a message to pre-determined channels")
async def announce(interaction: discord.Interaction, message: str):
    await log(interaction)  # Log the interaction
    author_id = str(interaction.user.id)
    await interaction.response.defer()

    # Check if the user is authorized to send announcements
    if not responses.ctxauthCheck(author_id)[0] and not responses.ctxauthCheck(author_id)[1]:
        await interaction.followup.send(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
        return

    else:
        # Extract the message content from the interaction (after '/announce ')
        try:
            echo_message = message  # The message after the command
        except IndexError:
            await interaction.followup.send(content="```ansi\n[0;31mERROR 22 - No announcement message provided.```", ephemeral=True)
            return

        # List of servers and channels to send the announcement
        sList = [1308416141227462697, 1308416160240504883, 1250296922816643136, 1312282745644519474]
        sListLen = len(sList) - 1

        try:
            while sListLen > -1:
                server_id = sList[sListLen]
                channel = bot.get_channel(server_id)
                if channel:
                    await channel.send(f"{echo_message} \n-# Announcement from: {interaction.user.display_name} - {interaction.guild}")
                sListLen -= 1
            await interaction.followup.send(f'```Your message has successfully been transmitted!```')

        except Exception as e:
            print(f"Error sending announcement: {e}")
            await interaction.followup.send(content="```ansi\n[0;31mERROR 21, no clue what happened, use '.issue'```", ephemeral=True)


# @bot.tree.command(name="say")
# async def say(interaction: discord.Interaction, message: str):
#     # Check if the user is authorized (by their user ID)
#     await log(interaction)
#     if interaction.user.id != 705669396999176233:
#         await interaction.response.send_message(content="Don't tell me what to do.")
#     else:
#         # Extract the message content from the interaction
#         try:
#             echo_message = str(message)  # Get the message from the slash command input
#         except IndexError:
#             await interaction.response.send_message(content="No message provided to echo.", ephemeral=True)
#             return
#
#         # Send the echo message
#         await interaction.channel.send(echo_message)


@bot.tree.command(name="unannounce", description="Unannounces the last successful announcement")
async def unannounce(interaction: discord.Interaction):
    await log(interaction)

    # Check for authorization
    if not responses.ctxauthCheck(str(interaction.user.id))[0]:
        await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        await interaction.response.defer()
        sList = [1312282745644519474, 1308416141227462697, 1308416160240504883, 1250296922816643136]
        sListLen = len(sList)
        sListLen -= 1

        # Loop through servers and delete the announcement message
        while sListLen > -1:
            server = sList[sListLen]
            channel = bot.get_channel(server)

            # Ensure the channel is valid
            if channel:
                async for message in channel.history(limit=20):
                    if message.author == bot.user:
                        await message.delete()
                        break

            sListLen -= 1

        # Send response back to the user
        await interaction.followup.send(content="```The previous announcement has now been deleted!```")


@bot.tree.command(name="bulkdelete", description="Deletes the specified number of messages in the channel")
async def bulkDelete(interaction: discord.Interaction, number: int):
    await log(interaction)
    await interaction.response.defer()

    # Check for authorization
    if not responses.ctxauthCheck(str(interaction.user.id))[1]:
        await interaction.followup.send(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")
    else:
        # Extract the number of messages to delete from the command arguments
        try:
            lim = int(number)  # Get the number from the message content
        except (IndexError, ValueError):
            await interaction.followup.send(content="Please provide a valid number of messages to delete.", ephemeral=True)
            return

        # Fetch the messages in the channel
        messages = [message async for message in interaction.channel.history(limit=lim)]
        if not messages:
            await interaction.followup.send(content="No messages found, or insufficient permissions", ephemeral=True)
        else:
            await interaction.followup.send(f"Deleted {len(messages)} messages.")
            await interaction.channel.delete_messages(messages)


async def modalFile(interaction: discord.Interaction, respondant, subject, action, reason, evidence, guild):
    print(guild)
    if guild == 1312282596734144522 or guild == 1276370934466351158 or guild == 1165355892842180641:
        print("TEST SERVER")
        emptyRow = testData.find("", in_column=4,).row
        testData.update_cell(emptyRow, 2, respondant)
        testData.update_cell(emptyRow, 4, subject)
        testData.update_cell(emptyRow, 6, action)
        testData.update_cell(emptyRow, 7, reason)
        if evidence:
            testData.update_cell(emptyRow, 8, evidence)


    elif guild == 1037423645548609586:
        print("vta")
    elif guild == 992284874591445033:
        print("vpd")
    elif guild == 932789384430886933:
        print("vgg")
    elif guild == 993550709347864576:
        print("vau")
    elif guild == 1017178557560143952:
        print("deptru")


class LogModal(ui.Modal, title="Logging Modal"):
    respondant = ui.TextInput(
        label="Username",
        placeholder="ex: MyName123"
    )
    subject = ui.TextInput(
        label="Subject\'s Roblox User",
        placeholder="ex: NotMyName123"
    )
    action = ui.TextInput(
        label="Action taken",
        placeholder="ex: Strike, Blacklist, etc..."
    )
    reason = ui.TextInput(
        label="Reason/description",
        placeholder="Leaking, AA, etc..."
    )
    evidence = ui.TextInput(
        required=False,
        label="Evidence (optional)",
        placeholder="https://..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if responses.ctxauthCheck(str(interaction.user.id))[1] or responses.ctxauthCheck(str(interaction.user.id))[0]:
            guild = interaction.guild.id
            await modalFile(interaction, str(self.respondant), str(self.subject), str(self.action), str(self.reason), str(self.evidence), guild)
            await interaction.followup.send(content=f"```ansi\n[0;32mSuccesfully submitted![0;0m\n\nSubject: {self.subject}\nAction: {self.action}\nReasoning: {self.reason}[0;0m```", ephemeral=False)
        else:
            await interaction.followup.send(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")

    async def on_error(self, interaction: discord.Interaction, error: Exception, traceback=None) -> None:
        await interaction.followup.send('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.tree.command(name="file", description="Use to open a Modal for punishment logging")
async def file(interaction: discord.Interaction):
    await log(interaction)
    await interaction.response.send_modal(LogModal())


async def infoGet2(subject, org):
    # Find all cells that contain the subject
    found_cells = org.findall(subject, in_column=4, case_sensitive=False)
    if not found_cells:
        return None
    row_numbers = [cell.row for cell in found_cells]
    temp1 = 0
    temp = []
    while temp1 <= int(len(row_numbers)) - 1:
        temp.append("\n" + str(subject))
        temp.append("\n" + str(org.cell(row_numbers[temp1], 5).value))
        temp.append("\n" + str(org.cell(row_numbers[temp1], 6).value))
        temp.append("\n" + str(org.cell(row_numbers[temp1], 7).value))
        if org.cell(row_numbers[temp1], 8).value:
            temp.append("\n" + str(org.cell(row_numbers[temp1], 8).value))
        temp1 += 1
    return temp


@bot.tree.command(name="change", description="Developer only")
async def change(interaction: discord.Interaction, stat: str):
    if interaction.user.id == 705669396999176233:
        if stat == "idle":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/commands"), status=discord.Status.idle)
        if stat == "dnd":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/commands"), status=discord.Status.dnd)
        if stat == "online":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/commands"), status=discord.Status.online)
        if stat == "offline":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/commands"), status=discord.Status.offline)
        await interaction.response.send_message(content=f"```ansi\n[0;32mSuccessfully changed bot presence to {stat}[0;0m```", ephemeral=True)
    else:
        await interaction.response.send_message(content="```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```")


bot.run(DISCORD_TOKEN)
