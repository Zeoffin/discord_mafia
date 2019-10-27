import random
import discord
import Player
import Mafia
import Villager
import Doctor
import asyncio
import os

token_path = open("E:/mafia_bot_token.txt", "r")
token = token_path.readline()
print("Token: {}".format(token))

client = discord.Client()

# The list of player names and player unique discord ID's
players_names = []
players_id = []
players_list = []
author_list = []

day = True

# On ready event- happens when bot is started up
@client.event
async def on_ready():

    print("Bot ready\n")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # Lets the users see the players that will be playing the game
    if message.content.startswith("!players"):

        names_list = ""
        count = 1

        if not players_names:
            await message.channel.send("No one has joined yet")
            return

        for i in players_names:
            names_list += "{}) ".format(count)
            names_list += str(i)
            names_list += "\n"
            count += 1

        print(players_id)
        await message.channel.send(names_list)

    # Lets users join the game
    if message.content.startswith('!join'):

        # Checks if user has already joined
        for i in players_id:
            if i == message.author.discriminator:
                await message.channel.send("{} already had joined".format(message.author.name))
                return

        # Make an Player object
        player = Player.Player(message.author.name, message.author.discriminator, None, True)

        # Places them into lists
        players_list.append(player)
        author_list.append(message.author)

        print(players_list)
        print(player.name)
        print(player.discriminator)

        players_names.append(player.name)
        players_id.append(player.discriminator)
        await message.channel.send("Joined next game")

    # Starts the game
    if message.content.startswith('!mafia'):

        # Get count of all members
        player_count = len(players_names)

        # TODO: COMMENT BACK WHEN READY !
        #if player_count < 4:
        #    await message.channel.send("Not enough players. Minimum of 4 is recommended.")
        #    return

        # Format all joined members
        count = 1
        names_list = ""

        for i in players_names:
            names_list += "{}) ".format(count)
            names_list += str(i)
            names_list += "\n"
            count += 1

        await message.channel.send('Game Starting with these members:\n {}'.format(names_list))

        # Assign each role number of players
        mafia_count = 1
        villager_count = 2
        doctor_count = 1

        if player_count == 5:

            mafia_count += 1

        elif player_count == 6:

            mafia_count += 1
            villager_count += 1

        elif player_count == 7:

            mafia_count += random.randint(0, 2)

            if mafia_count == 2:

                villager_count += 2

            elif mafia_count == 3:

                villager_count += 1

        # Give randomly roles to players
        mafia_id = 1
        villager_id = 2
        doctor_id = 3

        for player in players_list:

            role_picked = False

            while not role_picked:

                random_int = random.randint(0, 3)

                if random_int == mafia_id and mafia_count > 0:

                    player.role = Mafia.Mafia.role_name
                    mafia_count -= 1
                    role_picked = True

                elif random_int == villager_id and villager_count > 0:

                    player.role = Villager.Villager.role_name
                    villager_count -= 1
                    role_picked = True

                elif random_int == doctor_id and doctor_count > 0:

                    player.role = Doctor.Doctor.role_name
                    doctor_count -= 1
                    role_picked = True

        # Send assigned roles to players
        for author in author_list:

            player_string = ""
            role = ""
            player_name = ""
            author_string = str(author)

            # Make a string from a player object
            for player in players_list:

                player_string += player.name
                player_string += "#"
                player_string += player.discriminator

                player_name += player.name
                role += player.role

            if author_string == player_string:
                await author.send("Player name: {}\nYour role is: {}".format(player_name, role))


        for player in players_list:
            print("Name: {} and role: {}\n".format(player.name, player.role))


client.run(token)
