import disnake
from disnake.ext import commands

class MPCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('🔩 /mp command has been loaded')

    @commands.slash_command(name="mp", description="Send a private message to a user")
    @commands.has_permissions(manage_messages=True)
    async def send_mp(self, ctx, user: disnake.User, *, message: str):
        author = ctx.author

        try:
            embed = disnake.Embed(
                title=f"New Message from {author}",
                description=message,
                color=disnake.Color.old_blurple()
            )
            await user.send(embed=embed)
            response_embed = disnake.Embed(
                title="Message Sent",
                description=f"The message has been sent to {user.name}.",
                color=disnake.Color.green()
            )
            await ctx.send(embed=response_embed)

            # Wait for response in the DM
            def check(m):
                return m.author == user and isinstance(m.channel, disnake.DMChannel)

            response = await self.bot.wait_for("message", check=check)

            # Send the response to the author
            response_embed = disnake.Embed(
                title=f"Response from {user.name}",
                description=response.content,
                color=disnake.Color.old_blurple()
            )
            await author.send(embed=response_embed)

        except disnake.HTTPException:
            response_embed = disnake.Embed(
                title="Error",
                description="An error occurred while sending the message.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=response_embed)

def setup(bot):
    bot.add_cog(MPCommand(bot))