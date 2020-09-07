#!/usr/bin/python3
# https://discordapp.com/oauth2/authorize?client_id=508031670847275044&scope=bot&permissions=8

import discord
from discord.ext import commands
import asyncio
import logging
import datetime
import sys
import json

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = open("token.txt","r").read()
bot = commands.Bot(command_prefix='?', case_insensitive=True)


def community_report(guild): # function for user data
	online = 0
	idle = 0
	offline = 0

	for m in guild.members:
		if str(m.status) == "online":
			online += 1
		if str(m.status) == "offline":
			offline += 1
		else:
			idle += 1

	return online, idle, offline


# bot commands
@bot.command()
async def test(ctx, arg):
	await ctx.send(arg)


@commands.command()
async def ping(ctx):
	await ctx.send(str(bot.latency) + ' ms')

@bot.command()
async def purge(ctx, *, number:int=None):
#	await ctx.channel.purge(limit=amount)
	if ctx.message.author.guild_permissions.manage_messages:
		try:
			if number is None:
				await ctx.send("You must imput a number")
			else:
				deleted = await ctx.message.channel.purge(limit=number)
				await ctx.send(f"Messages purged by {ctx.message.author.mention}: `{len(deleted)}`")
		except:
			await ctx.send("I can't purge messages right now.")
	else:
		await ctx.send("You don't have permissions to use this command.")


@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f"Banned {member.mention}")

@bot.command()
async def unban(ctx, *, member):
	banned_users.ban(reason=reason)
	member_name, member_discriminator = member.split("#")

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discrimintaor) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"Unbanned {user.mention}")
			return


# bot events
@bot.event  # event decorator/wrapper
async def on_ready():
	print(f"{bot.user} has logged in.")


# member joining or leaving
@bot.event
async def on_member_join(member):
	for channel in member.server.channels:
		if str(channel) == "main-chat":
			await bot.send_message(f"""Welcome to =! 1337 server! {member.mention}""")
	#when new user join the server, we wanna set its xp & lvl to 0
	with open('users.json', 'r') as f: #so we gotta load the json file
		users = json.load(f)

	await update_data(users, member)

	with open('users.json', 'w') as f: #and set the new user into the json file
		json.dump(users, f)

@bot.event
async def on_member_remove(member):
	for channel in member.server.channels:
		if str(channel) == "main-chat":
			await bot.send_message(f"""{member.mention} rage quit!""")


@bot.event
async def on_message(message):
	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
	guild = message.channel.guild  #guild = bot.get_guild(392161068396576768)

	await bot.process_commands(message)

	if "duck_count" == message.content.lower():
		await message.channel.send(f"```py\n{guild.member_count}```")

	if "duck_report" == message.content.lower():
		online, idle, offline = community_report(guild)
		await message.channel.send(f"```Online: {online}.\nIdle/busy/dnd: {idle}.\nOffline: {offline}```")

	if "1337" in message.content.lower():
		await message.channel.send("you wish skid.")

	elif "oof" in message.content.lower():
		await message.channel.send("chill gin")

	if(message.author.id != 508031670847275044):
		#on every msg we wanna update the user's xp
		with open('users.json', 'r') as f:
			users = json.load(f)

		await update_data(users, message.author) #update the user's data in the json file
		await add_xp(users, message.author, 5) #soon will be change to random num
		await level_up(users, message.author, message)

		with open('users.json', 'w') as f:
			json.dump(users, f)


@bot.event # reposts messages that user deletes
async def on_message_delete(message):
	if message.author != bot.user:
	#if "$clear" == message.content.lower():
		await message.channel.send(f"@{message.author} Why did you delete: ```{message.content}```")

		await bot.process_commands(message)

@bot.event # changes nickname if value is set to sukhoi
async def on_member_update(before, after):
	n = after.nick
	if n:
		if n.lower().count("sukhoi") > 0:
			last = before.nick
			if last:
				await after.edit(nick=last)
			else:
				await after.edit(nick="You're not Duck Master")

"""
ranking system yo yo
"""
@bot.event
async def update_data(users, user):
	print(str(user.id) in users)
	if not str(user.id) in users:
		users[str(user.id)] = {} #create new user in the json
		users[str(user.id)]['xp'] = 0 #set the new user's xp to 0
		users[str(user.id)]['level'] = 1 #set the new user's level to 0
@bot.event
async def add_xp(users, user, xp):
	print(type(users[str(user.id)]['xp']))
	users[str(user.id)]['xp'] += xp
@bot.event
async def level_up(users, user, msg):
	xp = users[str(user.id)]['xp']
	level_start = users[str(user.id)]['level']
	level_end = int(xp ** (1/4))

	if level_start < level_end:
		await msg.channel.send('{} has leveled up to level {}'.format(user.mention, level_end))
		users[str(user.id)]['level'] = level_end



bot.run(token)
