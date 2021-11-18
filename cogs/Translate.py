import discord
from discord.ext import commands
from googletrans import Translator
import os
from dotenv import load_dotenv

load_dotenv(".env")

translator = Translator(service_urls=[
      "translate.google.com",
    ])

class Translate(commands.Cog):
    # Reference to the client from the main file
    def __init__(self, client):
        self.client = client

    # Run at start
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")

    # Command example
    @commands.command()
    async def testflag(self, ctx):
        flag = ctx.message.content.replace("!testflag ", "")
        msg = ""
        flags = ["af","al","am","ar","am","az","white","be","bn","bs","bg","ca","ph","cn","cn","cn","co","hr","cz","dk","nl","us","white","et","fi","fr","white","gl","ge","de","gr","gu","ht","ng","white","il","in","la","hu","is","ng","id","ga","it","jp","id","kn","kz","km","rw","kr","white","ky","la","lv","lt","lb","mk","mg","ms","ml","mt","white","mr","mn","my","ne","no","zm","in","ps","ir","pl","pt","pa","ro","ru","sm","gd","sr","st","sn","sd","si","sk","sl","so","es","sd","ke","sv","tl","tg","ta","tt","white","th","tr","tk","ua","pk","ug","uz","vi","cy","za","white","ng","za"]
        for i in range(len(flags)):
            msg = msg + f":flag_{flags[i]}:"
        await ctx.send(msg)

    # Read all messages
    @commands.Cog.listener()
    async def on_message(self, message):
    # Ignore messages coming from the bot
        if message.author == self.client.user :
            return

        elif not message.content[0].isalpha() and not message.content[0].isnumeric() and not message.content[0] == "<":
            return 

        elif not "lang=en" in str(translator.detect(message.content)):

            language =  str(translator.detect(message.content)).replace("Detected(lang=", "").replace(", confidence=None)", "")

            translations = translator.translate(message.content, dest='en')
            
            translationsText = str(translations.text)

            if "<@ " in translationsText :
                translationsText = translationsText.replace("<@ ", "<@")

            language = os.getenv(language)

            await message.channel.send(f"`{message.author.name}` {translationsText}       :flag_{language}: *{translations.origin}*")
            if (len(message.attachments) <= 0) :
                await message.delete()

# Function to connect this file to the bot
def setup(client):
    client.add_cog(Translate(client)) 

