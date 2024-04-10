import json
import os
from io import BytesIO

import disnake
from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw


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

            filename = "assets/jbanner_finish.png"
            background = Image.open("assets/join_banner.png")
            asset = member.display_avatar.with_size(1024)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp = WelcomeCog.circle(pfp)
            background.paste(pfp, (29, 12), pfp)
            background.save(filename)

            join_channel_id = config["JOIN_ID"]
            join_channel = self.bot.get_channel(join_channel_id)
            if join_channel:
                with open(filename, 'rb') as f:
                    file = disnake.File(f, filename=filename)
                    embed = disnake.Embed(
                        title=f"Dites bonjour a {member.display_name} !",
                        description=f"On est heureux de t'avoir ici **{member.mention}**!\n\nGrace a toi on est `{len(member.guild.members)}` membres !\n\nSoyez **heureux** et **profitez** du serveur !",
                        color=disnake.Color.blurple()
                        )
                    embed.set_image(url=f"attachment://{filename}")
                    msg = await join_channel.send(content=member.mention, file=file, embed=embed)
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
                title=f"Dites au revoir a {member.display_name}",
                description=f"Nous sommes tristes de te voir partir {member.mention}!\n\nSans toi, nous sommes maintenant {len(member.guild.members)} membres!\n\nNous espérons vous revoir tard",
                color=disnake.Color.brand_red()
                )
            await leave_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))