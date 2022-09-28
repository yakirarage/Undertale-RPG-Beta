import disnake
from disnake.ext import commands
import asyncio
from utility.dataIO import fileIO

class Cratesbtn(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @disnake.ui.button(label="Standard crate", style=disnake.ButtonStyle.secondary)
    async def standard(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "standard crate"
        self.stop()
    
    @disnake.ui.button(label="Determination crate", style=disnake.ButtonStyle.secondary)
    async def determination(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "determination crate"
        self.stop()
    
    @disnake.ui.button(label="Soul crate", style=disnake.ButtonStyle.secondary)
    async def soul(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "soul crate"
        self.stop()

    @disnake.ui.button(label="Void crate", style=disnake.ButtonStyle.secondary)
    async def void(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "void crate"
        self.stop()

    @disnake.ui.button(label="Event crate", style=disnake.ButtonStyle.secondary)
    async def event(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.value = "event crate"
        self.stop()


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Open your crates!")
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def crates(self, inter):
        data = await inter.bot.players.find_one({"_id": inter.author.id})
        standard = data["standard crate"]
        determin = data["determination crate"]
        soul = data["soul crate"]
        void = data["void crate"]
        event = data["event crate"]
        embed = disnake.Embed(
            title="Your crates",
            description="You can earn crates by exploring, voting, defeating bosses or in events",
            color=0x0077ff,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="Your boxes",
            value=f"""
Standard crates: {standard}
Determination crates: {determin}
Soul crates: {soul}
Void crates: {void}
Event crates: {event}
            """
        )
        embed.add_field(
            name="How to get",
            value=f"""
(Voting)
(/explore)
(Bosses)
(Resets)
(Events)
            """
        )

        view = Cratesbtn()
        await inter.send(view=view, embed=embed, ephemeral=True)

        await view.wait()
        if view.value == None:
            return await inter.edit_original_message("You took to long to reply!")
        else:
            crates = fileIO("data/crates.json", "load")
            if data[view.value] <= 0:
                return await inter.edit_original_message(
                    content=f"You don't have any **{view.value}**",
                    embed=None,
                    components=[]
                )
            
            data[view.value] -= 1
            earned_gold = crates[view.value]["gold"] * data["multi_g"]
            gold = data["gold"] + earned_gold

            info = {"gold": gold, view.value: data[view.value]}
            await inter.bot.players.update_one({"_id": inter.author.id}, {"$set": info})

            await inter.edit_original_message(
                content=f"You opened a **{view.value}**...",
                embed=None,
                components=[]
            )

            await asyncio.sleep(3)
            await inter.edit_original_message(
                content=f"You earned **{round(earned_gold)}G** from a **{view.value}**"
            )

def setup(bot):
    bot.add_cog(Shop(bot))