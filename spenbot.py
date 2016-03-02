import discord
import asyncio
import os
import random
import configparser

client = discord.Client()



@client.event
async def on_message(message):
	#instant invite
	if message.content.startswith('!invite'):
		await client.send_message(message.channel, 'Invite link: https://discord.gg/idkwhaturcodeis')


	#colour change
	elif message.content.startswith('.purple'):
                await client.replace_roles(message.author, discord.Object('131783428717805568'))
	elif message.content.startswith('.yellow'):
                await client.replace_roles(message.author, discord.Object('131783334106890241'))
	elif message.content.startswith('.green'):
                await client.replace_roles(message.author, discord.Object('131783248475979776'))
	elif message.content.startswith('.orange'):
                await client.replace_roles(message.author, discord.Object('131751014859538432'))
	elif message.content.startswith('.blue'):
		await client.replace_roles(message.author, discord.Object('131764686537490432'))
	elif message.content.startswith('.darkblue'):
		await client.replace_roles(message.author, discord.Object('131765882924826624'))
	elif message.content.startswith('.red'):
		await client.replace_roles(message.author, discord.Object('131751066051018752'))
	

	#radio list management
	elif message.content.startswith('!radio addsong'):
		songurl = False
		try:
			songurl = message.content.split(' ')[2]
		except:
			await client.send_message(message.channel, 'No song link specified')
		if songurl != False:
			songinlist = False
			songinsuggest = False

			with open('/home/spencer/projects/discord/musicbot/config/backuplist.txt') as backuplist:	
				for line in backuplist:
					if songurl in line:
						songinlist = True
			if songinlist == True:
				await client.send_message(message.channel, 'This song is already in the radio playlist')
			else:
				with open('/home/spencer/projects/discord/spenbot/radiosuggestions.txt') as radiosuggestions:
					for line in radiosuggestions:
						if songurl in line:
							songinsuggest = True
				if songinsuggest == True:
					await client.send_message(message.channel, 'This song has already been suggested')
				else:
					radiosuggestions = open('/home/spencer/projects/discord/spenbot/radiosuggestions.txt', 'a')
					radiosuggestions.write(songurl + '\n')
					await client.send_message(message.channel, 'Song suggestion submitted and awaiting approval before implementation.')
					radiosuggestions.close()

	elif message.content.startswith('!radio delsong'):
		songurl = False
		try:
			songurl = message.content.split(' ')[2]
		except:
			await client.send_message(message.channel, 'No song link specified')
		if songurl != False:
			songinlist = False
			songinsuggest = False

			with open('/home/spencer/projects/discord/musicbot/config/backuplist.txt') as backuplist:
				for line in backuplist:
					if songurl in line:
						songinlist = True			
							
			with open('/home/spencer/projects/discord/spenbot/radioremovals.txt') as radioremovals:
				for line in radioremovals:
					if songurl in line:
						songinsuggest = True				

			radioremovals = open('/home/spencer/projects/discord/spenbot/radioremovals.txt', 'a')
			if songinlist == False and songinsuggest == False:
				await client.send_message(message.channel, 'Song not in radio playlist')
				radioremovals.write(songurl + '\n')
			
			elif songinlist == True and songinsuggest == False:
				radioremovals.write(songurl + "\n")
				await client.send_message(message.channel, 'Song removal request submitted and awaiting approval before implementation')

			else:
				await client.send_message(message.channel, 'Removal request for this song already submitted')

			radioremovals.close()
	
	
	#points game
	elif message.content.startswith('!roll'):
		winorlose = random.randint(0,6)

		Config = configparser.ConfigParser()
		Config.read('/home/spencer/projects/discord/spenbot/points.ini')
		points = int(Config.get('Points', str(message.author)))
		
		if winorlose <= 4:
			points += 50
			Config.set('Points', str(message.author), str(points))
			with open('/home/spencer/projects/discord/spenbot/points.ini', 'w') as pointsfile:
				Config.write(pointsfile)
			await client.send_message(message.channel, str(message.author) + ', you win! You now have ' + str(points) + ' points!')
		
		else:
			points = points - 100
			Config.set('Points', str(message.author), str(points))
			with open('/home/spencer/projects/discord/spenbot/points.ini', 'w') as pointsfile:
				Config.write(pointsfile)
			await client.send_message(message.channel, str(message.author) + ', you lose :\'(. You now have ' + str(points) + ' points.')
	

	
	elif message.content.startswith('!playpoints'):
		Config = configparser.ConfigParser()
		Config.read('/home/spencer/projects/discord/spenbot/points.ini')

			
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('----')

client.run('email', 'pass')
