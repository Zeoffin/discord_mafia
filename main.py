""""

Discord bot made for playing the well known party game 'Mafia'.
discord.py is used for communicating with discord.

Made by: Zeoffin

"""

# Imports
import random
import discord
import Player
import Mafia
import Villager
import Doctor
import asyncio

# This is the path of token for the specific bot
token_path = open("E:/mafia_bot_token.txt", "r")
token = token_path.readline()

print("Initializing bot")

# Make a client object
client = discord.Client()

# The list of player names and player unique discord ID's
players_names = []
players_id = []
players_list = []
author_list = []

# Global variable for night
night = False

# Global player that will be killed
victim_name = ""

# List of assigned roles
mafia_list = []
mafia_names_list = []


# Global night variable, used in main game loop
def set_night_to_true():
    global night
    night = True


def set_night_to_false():
    global night
    night = False


# The player that will be killed at night
def victim_name_function(s):

    global victim_name
    victim_name += s


# On ready event- happens when bot is started up
@client.event
async def on_ready():

    print("Bot ready\n")


# on_message happens when discord user writes specific commands for the bot
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # The command for mafia to kill
    if message.content.startswith("!kill"):

        for i in mafia_list:

            # Make sure only those who are mafia can use the '!kill' command
            print(i)
            if str(i) != str(message.author):
                return

            # Check if it is night time or not
            elif str(i) == str(message.author) and not night:
                await message.author.send("You can only vote to kill during the night.")

            elif str(i) == str(message.author) and night:

                string_split = str(message.content).split(' ')
                victim_name_function(string_split[1])

                # Check if input is correct
                for player in players_names:

                    if player.name == victim_name and player.alive and player.role != Mafia.Mafia.role_name:
                        print("Player to be killed: {}".format(victim_name))

    # Lets the users see the players that will be playing the game
    if message.content.startswith("!players"):

        names_list = ""
        count = 1

        if not players_names:
            await message.channel.send("No one has joined yet")
            return

        # Returns all the players ready for the next game of mafia
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

        # Make an Player object.  None - role to be assigned later.  True - default alive status
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

        # Get the list of all players that are about to start playing the game
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
        for player in players_list:

            player_string = ""
            role = ""
            player_name = ""

            player_string += player.name
            player_string += "#"
            player_string += player.discriminator

            player_name += player.name
            role += player.role

            # Make a string from a player object
            for author in author_list:

                author_string = str(author)

                if author_string == player_string:

                    await author.send("Player name: {}\nYour role is: {}".format(player_name, role))
                    print("Sending roles")

                    # If a player gets the mafia role, add it to the list of all mafias
                    if player.role == Mafia.Mafia.role_name:
                        mafia_list.append(author)
                        mafia_names_list.append(player.name)

        # Send the mafia all other members of their team
        for mafia in mafia_list:

            mafia_string = ""
            count = 1

            for i in mafia_names_list:
                mafia_string += "{}) {}\n".format(count, i)
                count += 1

            await mafia.send("All Mafia members:\n" + mafia_string)

        # for debugging reasons
        for player in players_list:
            print("Name: {} and role: {}\n".format(player.name, player.role))

        await asyncio.sleep(3)
        await message.channel.send("The first night is coming soon!")
        await asyncio.sleep(10)

        # THE GAME LOOP

        game_going = True
        night_count = 1

        while game_going:

            # Night

            await message.channel.send("The night is about to begin!")
            await asyncio.sleep(3)
            await message.channel.send("Night {}".format(night_count))

            set_night_to_true()

            for mafia in mafia_list:

                count = 1
                not_mafia_string = ""

                for player in players_list:

                    if player.alive is True and player.role is not Mafia.Mafia.role_name:
                        not_mafia_string += "{}) {}\n".format(count, player.name)
                        count += 1

                await mafia.send("To kill a player, type !kill 'name', where 'name' is a player's name from the list below:\n"
                                 + not_mafia_string + "\n Player with the most votes will be killed this night.")

            await asyncio.sleep(20)
            await message.channel.send("Night time! 10 seconds remaining!")
            await asyncio.sleep(5)

            for i in range(5, 0, -1):

                if i == 1:
                    await message.channel.send("Night ending soon! 1 second remaining!")

                else:
                    await message.channel.send("Night ending soon! {} seconds remaining!".format(i))

                await asyncio.sleep(1)

            night_count += 1

            await message.channel.send("It is day time!")

client.run(token)
