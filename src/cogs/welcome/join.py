import json
import os
from io import BytesIO

import disnake
from modules.var import *
from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw
from utils.load_lang import welcome_lang as langText



class JoinMessageUtils(commands.Cog):
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
        print('🧰 Join has been loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            with open(files.config, 'r') as config_file:
                config = json.load(config_file)

            filename = "assets/jbanner_finish.png"
            background = Image.open("assets/join_banner.png")
            asset = member.display_avatar.with_size(1024)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp = JoinMessageUtils.circle(pfp)
            background.paste(pfp, (29, 12), pfp)
            background.save(filename)

            join_channel_id = config["JOIN_ID"]
            join_channel = self.bot.get_channel(join_channel_id)
            if join_channel:
                with open(filename, 'rb') as f:
                    file = disnake.File(f, filename=filename)
                    embed = disnake.Embed(
                        title=langText.get("JOIN_TITLE").format(userName=member.display_name),
                        description=langText.get("JOIN_TEXT").format(userMention=member.mention, usersCount=len(member.guild.members)),
                        color=disnake.Color.blurple()
                        )
                    embed.set_image(url=f"attachment://{filename}")
                    msg = await join_channel.send(content=member.mention, file=file, embed=embed)
                    await msg.add_reaction("👋")
            try:
                os.remove(filename)
            except:
                pass


def setup(bot):
    bot.add_cog(JoinMessageUtils(bot))