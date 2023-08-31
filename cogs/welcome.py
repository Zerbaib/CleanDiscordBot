from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw
from io import BytesIO
import disnake, json, os

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def circle(pfp, size = (75,75)): 
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Join and leave ⚙️ ==========')
        print('🧰 Join has been loaded')
        print('🧰 Leave has been loaded')
        print()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)

            filename = "banner_finish.png"
            background = Image.open("banner.png")
            asset = member.display_avatar.with_size(1024)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp = self.circle(pfp)
            background.paste(pfp, (29, 12), pfp)
            background.save(filename)


            join_channel_id = config["JOIN_ID"]
            join_channel = self.bot.get_channel(join_channel_id)
            if join_channel:
                embed = disnake.Embed(
                    title=f"Say welcome to {member.display_name}!",
                    description=f"We are happy to have you here **{member.mention}**!\n\nWith you, we are now `{len(member.guild.members)}` members!\n\nBe **happy** and **enjoy** your stay !",
                    color=disnake.Color.blurple()
                    )
                embed.set_image(url="attachment://" + filename)
                msg = await join_channel.send(embed=embed)
                await msg.add_reaction("👋")
            try:
                os.remove(filename)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        leave_channel_id = config["LEAVE_ID"]
        leave_channel = self.bot.get_channel(leave_channel_id)
        if leave_channel:
            embed = disnake.Embed(
                title=f"Say goodbye to {member.display_name}",
                description=f"We are sad to see you leave {member.mention}!\n\nWith you, we are now {len(member.guild.members)} members!\n\nWe hope to see you again lat",
                color=disnake.Color.brand_red()
                )
            await leave_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))