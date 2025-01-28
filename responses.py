# imports
import time
from discord.ui import Button, View
from discord.ext import commands
import discord
import gspread
from discord import Client
from google.oauth2.service_account import (Credentials)

# API creds
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("Creds.json", scopes=scopes)
client = gspread.authorize(creds)


sheet_id2 = "1espNxTCzMOwAYnQyEnHjJmDT9aOTf6JtDfiY0mrqtFU"
workbook2 = client.open_by_key(sheet_id2)

# Specify worksheets
SensData = workbook2.get_worksheet(0)
authLevel1: str
authLevel2: str
authLevel3: str


def authUpdate():
    global authLevel1
    global authLevel2
    global authLevel3
    authLevel1 = str(SensData.cell(1, 2).value)
    authLevel2 = str(SensData.cell(2, 2).value)
    authLevel3 = str(SensData.cell(3, 2).value)


# def authCheck(level):
#     authUpdate()
#     if level == 3:
#         if Author in authLevel3:
#             return True
#
#     if level == 2:
#         if Author in authLevel2:
#             return True
#
#     if level == 1:
#         if Author in authLevel1:
#             return True
#         else:
#             return


def ctxauthCheck(ID):
    authUpdate()
    list = []
    if ID in authLevel3:
        list.append(True)
    if ID not in authLevel3:
        list.append(False)

    if ID in authLevel2:
            list.append(True)
    if ID not in authLevel2:
        list.append(False)

    if ID in authLevel1:
            list.append(True)
    if ID not in authLevel1:
        list.append(False)
    return list


# def infoGet(name):
#     if str(sheet.find(name)) == 'None' or str(sheet2.find(name)) == 'None' or str(sheet3.find(name)) == 'None':
#         return "```ansi\n[0;31mERROR 4 - Educator not found in employee database[0;0m```"
#
#     else:
#
#         # Classes hosted finder
#         asocRoster = str(sheet.find(name)).split('C')
#         asocRoster = asocRoster[1].split('R')
#         asocRoster = int(asocRoster[1])
#         val = str(sheet.cell(asocRoster, 9)).split('\'')
#         val = int(val[1])
#         # Incentive points finder
#         pointDatabase = str(sheet2.find(name)).split('C')
#         pointDatabase = pointDatabase[1].split('R')
#         pointDatabase = int(pointDatabase[1])
#         val1 = str(sheet2.cell(pointDatabase, 6)).split('\'')
#         val1 = int(val1[1])
#
#         # Passed civs finder
#         passCivs = str(sheet3.find(name)).split('C')
#         passCivs = passCivs[1].split('R')
#         passCivs = int(passCivs[1])
#         val2 = str(sheet3.cell(passCivs, 4)).split('\'')
#         val2 = str(val2)
#         val2 = int(val2.count('.'))
#
#         hosted = str(val)
#         points = str(val1)
#         passes = str(val2)
#         t = "Teacher - " + name + "\n Classes hosted - " + hosted + "\n Current points - " + points + "\n Students passed - " + passes
#         return '```ansi\n[0;37m' + str(t) + '[0;0m```'


# def classLog(teacher, passedcivs, failedcivs):
#     if not authCheck(1):
#         return error(4)
#     else:
#         if str(sheet2.find(teacher)) == 'None':
#             return error(2)
#         PD = str(sheet2.find(teacher)).split('C')
#         PD = PD[1].split('R')
#         PD = int(PD[1])
#         val1 = str(sheet2.cell(PD, 6)).split('\'')
#         val1 = float(val1[1])
#         val1 += 2
#         sheet2.update_cell(PD, 6, val1)
#
#         # ASSOCIATION ROSTER SHEET # NOQA
#         AR = str(sheet.find(teacher))
#         AR = AR.split('C')
#         AR = AR[1].split('R')
#         AR = int(AR[1])
#         val = str(sheet.cell(AR, 9)).split('\'')
#         val = val[1]
#         val = float(val) + 1
#         sheet.update_cell(AR, 9, val)
#
#         temp = "Teacher: " + str(
#             teacher) + ". \nPasses: " + passedcivs + ". \nFails: " + failedcivs + ' \nClasses hosted: ' + str(
#             val) + " \nIncentive points: " + str(val1)  # NOQA
#         temp = '```ansi\n[0;37m' + str(temp) + '[0;0m```'
#         return temp


# def console():
#     print(Author2 + " '" + Logged + "' " + Channel)


# def error(number):
#     console()
#     print(f'Above log ended in error {number}')
#     if number == 1:
#         return "```ansi\n[0;31mERROR 1 - inorrect # arguments[0;0m```"
#     if number == 2:
#         return "```ansi\n[0;31mERROR 2 - Educator not found in employee database[0;0m```"
#     if number == 3:
#         return "```ansi\n[0;31mERROR 3 - No special characters allowed in input[0;0m```"
#     if number == 4:
#         return "```ansi\n[0;31mERROR 4 - Non authorized user conducting a protected function.[0;0m```"
#     if number == 5:
#         return "```ansi\n[0;31mERROR 5 - Incorrect class type. Make sure you are inputting numbers/letters where expected[0;0m```"
#     if number == 6:
#         return "```ansi\n[0;31mERROR 6 - Bot access state 1, no access granted. DList users may reverse this using 'accessState0'.[0;0m```"
#     if number == 7:
#         return "```ansi\n[0;31mERROR 7 - Only Cirilla_dev may remove admins. Use '.end' to shut down the bot in-cases of  or AA. [0;0m```"



# def get_response(message, serverMessage):  # noqa
#
#     lowerMessage = serverMessage
#     lowerMessage = lowerMessage.lower()
#
#     # Author variable
#     global Author
#     global Author2
#     global Channel
#     global Logged
#     Author = str(message.author.id)
#     Author2 = str(message.author)
#     Channel = str(message.channel)
#     Logged = str(serverMessage)
#
#     # Re-checks if message from bot
#     if Author == '1250277804478562397':
#         return
#
#
#     if lowerMessage[:4] == 'get:':
#         name = serverMessage[5:]
#         console()
#         return infoGet(name)
#
#     if lowerMessage[:4] == 'log:':
#         temp = serverMessage[5:].split(',')
#         teacher = temp[0]
#         pCivs = temp[1]
#         fCivs = temp[2]
#         console()
#         return classLog(teacher, pCivs, fCivs)
