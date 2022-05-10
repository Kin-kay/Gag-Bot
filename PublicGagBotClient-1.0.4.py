import os
import random
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

#Level set to warning as info and debug are an absolute shit show. Only use info as a last resort. Only use Debug if you are insane. Log file is made in the directory where you ran the file.
logging.basicConfig(level=logging.WARNING,filename='Gagbot.log',filemode='a',
                    format="%(asctime)s - %(levelname)s - %(message)s")

#Token saved in .env file so as to not leave it in code.
load_dotenv()
logging.info("Obtaining Token from env")
TOKEN = os.getenv('DISCORD_TOKEN')
logging.info("Obtained Token from env")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
@commands.has_role('Owner')
#Gag
async def Gag(ctx, user: discord.Member):
    logging.warning("{} - {} used command Gag on {}.".format(ctx.message.guild.name, ctx.message.author, user))
    await ctx.send("Gagging: " + str(user))
    logging.info("{} - Finding role Gagged and Pet".format(ctx.message.guild.name))
    role = discord.utils.find(lambda r: r.name == 'Gagged', ctx.message.guild.roles)
    Pet = discord.utils.find(lambda r: r.name == 'Pet', ctx.message.guild.roles)
    logging.info("{} - Found role Gagged and Pet. Checking if mentioned user has the role.".format(ctx.message.guild.name))
    if role in ctx.author.roles:
        if user == ctx.author:
            logging.info("{} - {} is {} cancelling command.".format(ctx.message.guild.name,user,ctx.message.author))
            await ctx.send('You can\'t remove your own gag cutie')
        else:
            logging.info("{} - {} is Gagged cancelling command.".format(ctx.message.guild.name,ctx.message.author))
            await ctx.send('Gagged Pets should keep their paws to themselves.')
    else:
        if Pet in user.roles:
            if role in user.roles:
                await ctx.send("{} is gagged. Removing Gag.".format(user))
                await user.remove_roles(role)
            else:
                await ctx.send("{} is not gagged. Gagging.".format(user))
                await user.add_roles(role)
        else:
            await ctx.send("{} is not a pet.".format(user))
    logging.info("{} - Completed command Gag.".format(ctx.message.guild.name))

@bot.command()
@commands.has_role('Owner')
#Pet
async def Pet(ctx, user: discord.Member):
    logging.warning("{} - {} used command Pet on {}.".format(ctx.message.guild.name, ctx.message.author, user))
    await ctx.send("Collaring: " + str(user))
    logging.info("{} - Searching for role Pet".format(ctx.message.guild.name))
    Pet = discord.utils.find(lambda r: r.name == 'Pet', ctx.message.guild.roles)
    Gagged = discord.utils.find(lambda r: r.name == 'Gagged', ctx.message.guild.roles)
    logging.info("{} - Found role Pet".format(ctx.message.guild.name))
    if Pet in user.roles:
        logging.info("{} - {} has role Pet".format(ctx.message.guild.name, user))
        await ctx.send("{} is collared. Removing Collar.".format(user))
        await user.remove_roles(Pet)
        if Gagged in user.roles:
            await user.remove_roles(Gagged)
    else:
        logging.info("{} - {} does not have role Pet".format(ctx.message.guild.name, user))
        await ctx.send("{} is not collared. Collaring.".format(user))
        await user.add_roles(Pet)
    logging.info("{} - Completed command Pet.".format(ctx.message.guild.name))

@bot.command()
@commands.has_role('Owner')
#Setup
async def Startup(ctx):
    logging.warning("{} - {} has used command Startup.".format(ctx.message.guild.name,ctx.message.author))
    await ctx.send("Initializing Startup...")
    await ctx.send("Creating roles...")
    await ctx.message.guild.create_role(name="Pet")
    await ctx.message.guild.create_role(name="Gagged")
    role = discord.utils.find(lambda r: r.name == 'Gagged', ctx.message.guild.roles)
    Pet = discord.utils.find(lambda r: r.name == 'Pet', ctx.message.guild.roles)
    await ctx.send('Created role: {} and {}.'.format(role, Pet))
    await ctx.send("Startup Sequence Complete!")
    logging.info("{} - Completed command Startup.".format(ctx.message.guild.name))

@bot.command()
#Struggling
@commands.has_role('Gagged')
async def Struggle(ctx):
    logging.warning("{} - {} has used command Struggle".format(ctx.message.guild.name,ctx.message.author))
    await ctx.send('The Pet struggles at her gag.')
    if random.randint(0,5) == random.randint(0,5):
        await ctx.send('The Pet as struggled out of her gag! Bad girl!')
        role = discord.utils.find(lambda r: r.name == 'Gagged', ctx.message.guild.roles)
        await ctx.message.author.remove_roles(role)
    else:
        await ctx.send('The Pet struggles pitifully at her gag. Adorable.')
    logging.info("{} - Completed command Struggle.".format(ctx.message.guild.name))

@bot.command()
#Cleanup
@commands.has_role('Owner')
async def Cleanup(ctx,Amount):
    logging.warning("{} - {} has used command Cleanup to delete {} messages.".format(ctx.message.guild.name,ctx.message.author,Amount))
    if int(Amount) == 0:
        fail = await ctx.send ("Please enter an amount to delete!")
        await fail.delete()
    if int(Amount) >= 16:
        fail = await ctx.send("Your numbers are too big!")
        await fail.delete()
    else:
        Amount = (int(Amount) + 1)
        await ctx.channel.purge(limit=Amount)
    logging.info("{} - Completed command Cleanup.".format(ctx.message.guild.name))

@bot.command()
#Help
async def Help(ctx):
    logging.warning("{} - {} has used command Help".format(ctx.message.guild.name,ctx.message.author))
    await ctx.send("```Help:\n" +
                   "This bot was made for fun by Kin-kay\n" +
                   "Thanks for using!\n\n" +
                   "TO USE THIS BOT YOU MUST FIRST CREATE A ROLE CALLED \"Owner\" (without the \")\n\n" +
                   "Startup\n" +
                   "Run by tags: Owner\n" +
                   "This command must be run first!\n" +
                   "This command sets up the roles Pet and Gagged which are necessary for the bot to work.\n\n" +
                   "Pet (user)\n" +
                   "Run by tags: Owner\n" +
                   "This command gives the role Pet to (user) which allows for (user) to be gagged.\nNote that if (user) is not Pet they can not be gagged, removing Pet also removes gagged.\n\n" +
                   "Gag (user)\n" +
                   "Run by tags: Owner\n" +
                   "This command gives the role Gagged to (user) which the bot will check for when running the gagging section.\nNote (user) can not be gagged if they are not Pet.\nNote Gagged messages original contents are sent to log.\n\n" +
                   "Struggle\n" +
                   "Run by tags: Gagged\n" +
                   "This command checks if two random numbers both 0-6 are equal (1/32 chance). If they are then Gagged role is removed.\n\n" +
                   "Cleanup (int)\n" +
                   "Run by tags: Owner\n" +
                   "This command deletes (int)+1 messages, the +1 is so you don't have to include the command you send in the number of messages to delete. Min 1 Max 15\n" +
                   "```"
                   )
    logging.info("{} - Completed command Help.".format(ctx.message.guild.name))

@bot.event
#gagging
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    role = discord.utils.find(lambda r: r.name == 'Gagged', message.guild.roles)
    if role in message.author.roles:
        if not message.attachments:
            logging.warning("{} - {} - Gagged Message - {}".format(message.guild.name,message.author,message.content))
            wordlist = message.content.split()
            await message.delete()
            NumOWords = len(wordlist)
            i = 0
            Noises = ['Mmm','Mmmph','Mm','MMM','Mmmrph','Mmmgh','Mmmgph','Mmmmmmm','M','MMMPH','MMMGH','MMmmm']
            Noise = []
            while i != NumOWords:
                i += 1
                Noise.append(random.choice(Noises))
            GagNoises = ' '.join(Noise)
            await message.channel.send('The Gagged Pet tried to speak: \"' + GagNoises + '\"')
    await bot.process_commands(message)

bot.run(TOKEN)