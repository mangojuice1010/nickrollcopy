# Nickroll.py
#
# Implements practice timer in HCLC server's voice channels
# By: mintchoco
# 08/10/21
#

import os
import discord
import time
from re import search

# Discord bot token required to run
token = 'insert actual token here'
client = discord.Client()

# checks that bot is on and ready
@client.event
async def on_ready():
    print("Bot is up and running. Waiting for actions.")

@client.event
async def on_message(message):

    # make sure bot doesn't respond to its own messages to avoid infinite loop
    if message.author == client.user:
        return

    # converts msg to all lowercase for ease of calling functions
    msg = message.content.lower()
    print("")
    print('message received: ' + msg)
    print('from: ' + str(message.author.name))

    # bot responds to user being hungry
    if search("hungry", msg):
        await message.channel.send('_**KUNG PAO your CHICKEN**_ and _**MAPO your TOFU!!!**_')

    # if bot is mentioned, returns the functions the user can use
    for x in message.mentions:
        if(x==client.user):
            await message.channel.send(f"Hello, please type $practice to start timing your session, and $stop when you're done!")
            await message.channel.send("For the full command menu, type $help.")

    # if $help is attempted, returns list of usable commands
    if msg.startswith('$help'):
        await message.channel.send("__List of commands:__\n$practice to start timing your session\n$stop when you're done practicing\n$song to input current piece being practiced\n$pause to take a practice break\n$resume to resume practice after a break\n$time to check length of current session")

    # bot says hello when user says hello
    if 'hello' in msg:
        await message.channel.send('INHALE')
        await message.channel.send('INHALE INHALE')
        await message.channel.send('INHALE INHALE INHALE')
        await message.channel.send('_HUHUHUHUHUHUHUHUHUHUHUHUHUHUHUHUHU_')
        await message.channel.send('**HELLO!!!!! Привет!!!! 你好!!!!**')

    # implements $practice command to start timer
    if msg.startswith('$practice'):
        # if not already practicing
        if ('start' in globals()):
            await message.channel.send("Someone is already practicing.")
        else:
            if message.author.voice:
                await message.add_reaction('\N{fire}')
                await message.add_reaction('<:langlang:846295549410017280>')
                embed = discord.Embed(title= 'Supa Hot :fire: Get chop Chopin', color=discord.Color.blue(), description = 'Timer for ' + message.author.name + "'s practice session will start now")
                embed.set_image(url="https://media.giphy.com/media/Aff4ryYiacUO4/giphy.gif")
                await message.channel.send(embed=embed)

                global start
                start = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                global praccer
                praccer = str(message.author.name)
                global totalPauses
                totalPauses = 0
                global recentPause
                recentPause = 0
            else:
                await message.channel.send("You must join a voice channel to practice.")

    # implements $pause command to pause timer
    elif msg.startswith('$pause'):
        if not ('praccer' in globals()):
            await message.channel.send("You must be practicing to use this command.")
        elif (str(message.author.name) == praccer):
            if not message.author.voice:
                await message.channel.send("You are not in voice channel.")
            elif not ('start' in globals()):
                await message.channel.send("You are not currently practicing.")
            elif ('paused' in globals()):
                await message.channel.send("You are already paused.")
            else:
                pauseStart = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                await message.add_reaction('\N{smirking face}')
                await message.add_reaction('<:sus:846303596034129940>')
                embed = discord.Embed(title= "But I'm not a praccer", color=discord.Color.blue(), description = "Better $resume soon 'cause this praccing slaccing about to end this whole " + message.author.name + "'s career")
                embed.set_image(url="https://media.giphy.com/media/ZKh08mJr2cMHS/giphy.gif")
                await message.channel.send(embed=embed)

                # calculates start of pause
                startPauseHr = pauseStart[11:13]
                startPauseMin = pauseStart[14:16]
                startPauseSec = pauseStart[17:19]

                global startPauseTime
                startPauseTime = int(startPauseHr)*3600 + int(startPauseMin)*60 + int(startPauseSec)

                global paused
                paused = True
        else:
            await message.channel.send("You cannot pause " + praccer + "'s practice session!")

    # implements $resume command to resume timer
    elif msg.startswith('$resume'):
        if not ('praccer' in globals()):
            await message.channel.send("You must be practicing to use this command.")
        elif (str(message.author.name) == praccer):
            if not message.author.voice:
                await message.channel.send("You are not in voice channel.")
            if not ('paused' in globals()):
                await message.channel.send("You are not paused.")
            else:
                await message.add_reaction('\N{party popper}')
                await message.add_reaction('<:perfect:846303474723192852>')

                global pauseEnd
                pauseEnd = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

                # calculates total pause time
                endPauseHr = pauseEnd[11:13]
                endPauseMin = pauseEnd[14:16]
                endPauseSec = pauseEnd[17:19]

                global endPauseTime
                endPauseTime = int(endPauseHr)*3600 + int(endPauseMin)*60 + int(endPauseSec)

                del globals()['paused']

                # calculates time of this pause
                global pauseTotal
                if ('startPauseTime' in globals()):
                    pauseTotal = endPauseTime - startPauseTime
                    pauseHr =  pauseTotal // 3600
                    pauseMin = (pauseTotal % 3600) // 60
                    pauseSec = (pauseTotal % 3600) % 60

                    embed = discord.Embed(title= "OHHHHHH", color=discord.Color.blue(), description = 'Boom bam bap badabap boom pow commencing ' + message.author.name + "'s practice after a " + str(pauseHr) + " hr, " + str(pauseMin) + " min, and " + str(pauseSec) + " sec break")
                    embed.set_image(url="https://media.giphy.com/media/EsTZ0St3YdZfO/giphy.gif")
                    await message.channel.send(embed=embed)

                    totalPauses = totalPauses + pauseTotal
                    print(totalPauses)

                    # calculates total pauses used in one $song command
                    recentPause = recentPause + pauseTotal
                    pauseTotal = 0
                else:
                    message.channel.send("You forgot to pause.")
        else:
            await message.channel.send("You cannot resume " + praccer + "'s practice session!")

    # sets song or piece
    elif msg.startswith('$song'):
        if not ('praccer' in globals()):
            await message.channel.send("You are not currently practicing.")
          # if practicing, checks user
        elif ('start' in globals()):
            if (str(message.author.name) == praccer):
                  recentPause = 0
                  global song
                  song = message.content.split("$song ",1)[1]
                  songTime = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

                  startSongHr = songTime[11:13]
                  startSongMin = songTime[14:16]
                  startSongSec = songTime[17:19]

                  global songStart
                  songStart = int(startSongHr)*3600 + int(startSongMin)*60 + int(startSongSec)
                  await message.channel.send("Ok not bad, song set to " + song + ".")
            else:
                  await message.channel.send("Sorry, please wait for " + praccer + " to finish practicing.")
        else:
            await message.channel.send("You cannot choose the song in someone else's practice session.")

    # implements $time command to check current running total practice time
    elif msg.startswith('$time'):
        if not ('praccer' in globals()):
            await message.channel.send("You must be practicing to use this command.")
        elif ('praccer' in globals()) and (str(message.author.name) == praccer):
            if not message.author.voice:
                await message.channel.send("You are not in voice channel.")

            elif ('paused' in globals()):
                await message.channel.send("Your practice time will accurately update once you type $resume or $stop.")

            elif not ('start' in globals()):
                await message.channel.send("You are not currently practicing.")

            else:
                await message.add_reaction('\N{alarm clock}')
                await message.add_reaction('<:wao:846295335176765463>')

                startHr = start[11:13]
                startMin = start[14:16]
                startSec = start[17:19]

                current = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

                startTime = int(startHr)*3600 + int(startMin)*60 + int(startSec)

                currentHr = current[11:13]
                currentMin = current[14:16]
                currentSec = current[17:19]

                currentTime = int(currentHr)*3600 + int(currentMin)*60 + int(currentSec)

                currentNetSec = currentTime - startTime - totalPauses

                #print(totalSec) test line for calculation
                currentTotalHr =  currentNetSec // 3600
                currentTotalMin = (currentNetSec % 3600) // 60
                currentTotalSec = (currentNetSec % 3600) % 60

                desc = message.author.name + "'s current practice session is " + str(currentTotalHr) + " hr, " + str(currentTotalMin) + " min, and " + str(currentTotalSec) + " sec long."

                if ('song' in globals()):
                    songCurrentTime = currentTime - songStart

                    if ('recentPause' in globals()):
                        if ('startPauseTime' in globals() and startPauseTime > songStart):
                            songCurrentTime = currentTime - songStart - recentPause

                    songCurrentHr = songCurrentTime // 3600
                    songCurrentMin = (songCurrentTime % 3600) // 60
                    songCurrentSec = (songCurrentTime % 3600) % 60

                    desc = desc + "\nCurrent piece: " + song + ", for " + str(songCurrentHr) + " hr, " + str(songCurrentMin) + " min, and " + str(songCurrentSec) + " sec"
                embed = discord.Embed(title= "Not enough", color=discord.Color.blue(), description = desc)
                embed.set_image(url="https://media.giphy.com/media/iacwXyWu2bYTS/giphy.gif")
                await message.channel.send(embed=embed)
        else:
            await message.channel.send("Only the practicer can check the current practice session time.")

    # implements $stop command to stop timer
    elif msg.startswith('$stop'):
        if not ('praccer' in globals()):
                await message.channel.send("You must be practicing to use this command.")
        elif (str(message.author.name) == praccer):
            if not message.author.voice:
                await message.channel.send("You are not in voice channel.")
            if not ('start' in globals()):
                await message.channel.send("You are not currently practicing.")
            else:
                end = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

                await message.add_reaction('\N{teacup without handle}')
                await message.add_reaction('<:gnalgnal:846295440144203787>')

                startHr = start[11:13]
                startMin = start[14:16]
                startSec = start[17:19]

                startTime = int(startHr)*3600 + int(startMin)*60 + int(startSec)

                endHr = end[11:13]
                endMin = end[14:16]
                endSec = end[17:19]

                endTime = int(endHr)*3600 + int(endMin)*60 + int(endSec)

                global totalSec

                if 'pauseTotal' in globals():
                    totalSec = endTime - startTime - pauseTotal
                else:
                    totalSec = endTime - startTime - totalPauses

                # print(totalSec) test line for calculation
                praccHr =  totalSec // 3600
                praccMin = (totalSec % 3600) // 60
                praccSec = (totalSec % 3600) % 60

                praccTotal = str(praccHr) + ' hr, ' + str(praccMin) + ' min, and ' + str(praccSec) + ' sec of pracc'

                # embed final practice time message and info
                embed = discord.Embed(title= 'Never gonna give you up...', color=discord.Color.blue(), description = '...oof I gtg after ' + praccTotal + " :tea:")
                embed.set_image(url="https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif")
                await message.channel.send(embed=embed)

                # resets global variables for next practice session
                if 'startPauseTime' in globals():
                    del globals()['startPauseTime']
                if 'start' in globals():
                    del globals()['start']
                if 'pauseEnd' in globals():
                    del globals()['pauseEnd']
                if 'pauseTotal' in globals():
                    del globals()['pauseTotal']
                if 'totalSecYeet' in globals():
                    del globals()['totalSecYeet']
                if 'paused' in globals():
                    del globals()['paused']
                if 'praccer' in globals():
                    del globals()['praccer']
                if 'endPauseTime' in globals():
                    del globals()['endPauseTime']
                if 'song' in globals():
                    del globals()['song']
                if 'recentPause' in globals():
                    del globals()['recentPause']
                if 'totalPauses' in globals():
                    del globals()['totalPauses']
                if 'songStart' in globals():
                    del globals()['songStart']
                if 'totalSec' in globals():
                    del globals()['totalSec']
        else:
            await message.channel.send("You cannot stop " + praccer + "'s practice session!")

    @client.event
    async def on_voice_state_update(member, before, after):
        if before.channel is not None and after.channel is None:
            if ('praccer' in globals()) and (praccer == str(member.name)):
                await message.channel.send("Please use the $stop command before leaving voice channel when you finish practicing.")
                end = message.created_at.strftime('%Y-%m-%d %H:%M:%S')

                startHr = start[11:13]
                startMin = start[14:16]
                startSec = start[17:19]

                startTime = int(startHr)*3600 + int(startMin)*60 + int(startSec)

                endHr = end[11:13]
                endMin = end[14:16]
                endSec = end[17:19]

                endTime = int(endHr)*3600 + int(endMin)*60 + int(endSec)

                global totalSecYeet

                if 'pauseTotal' in globals():
                    totalSecYeet = endTime - startTime - pauseTotal
                else:
                    totalSecYeet = endTime - startTime - totalPauses

                # print(totalSecYeet) test line for calculation
                praccHr =  totalSecYeet // 3600
                praccMin = (totalSecYeet % 3600) // 60
                praccSec = (totalSecYeet % 3600) % 60

                praccTotal = str(praccHr) + ' hr, ' + str(praccMin) + ' min, and ' + str(praccSec) + ' sec of pracc'

                # embed final practice time message and info
                embed = discord.Embed(title= 'Never gonna give you up...', color=discord.Color.blue(), description = '...oof I gtg after ' + praccTotal + " :tea:")
                embed.set_image(url="https://media.giphy.com/media/Ju7l5y9osyymQ/giphy.gif")
                await message.channel.send(embed=embed)

                # resets global variables for next practice session
                if 'startPauseTime' in globals():
                    del globals()['startPauseTime']
                if 'start' in globals():
                    del globals()['start']
                if 'pauseEnd' in globals():
                    del globals()['pauseEnd']
                if 'pauseTotal' in globals():
                    del globals()['pauseTotal']
                if 'totalSecYeet' in globals():
                    del globals()['totalSecYeet']
                if 'paused' in globals():
                    del globals()['paused']
                if 'praccer' in globals():
                    del globals()['praccer']
                if 'endPauseTime' in globals():
                    del globals()['endPauseTime']
                if 'song' in globals():
                    del globals()['song']
                if 'recentPause' in globals():
                    del globals()['recentPause']
                if 'totalPauses' in globals():
                    del globals()['totalPauses']
                if 'songStart' in globals():
                    del globals()['songStart']
                if 'totalSec' in globals():
                    del globals()['totalSec']

client.run(token, bot=True)
