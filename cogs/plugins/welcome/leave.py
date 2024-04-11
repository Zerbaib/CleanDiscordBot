import json
import os
from io import BytesIO

import disnake
from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw

from cogs.utils.lang_loader import load_welcome_lang

langText = load_welcome_lang()

class LeaveMessageUtils(commands.Cog):
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
        print('🧰 Leave has been loaded')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)

            filename = "assets/lbanner_finish.png"
            background = Image.open("assets/leave_banner.png")
            asset = member.display_avatar.with_size(1024)
            data = BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            pfp = LeaveMessageUtils.circle(pfp)
            background.paste(pfp, (29, 12), pfp)
            background.save(filename)        

            leave_channel_id = config["LEAVE_ID"]
            leave_channel = self.bot.get_channel(leave_channel_id)
            if leave_channel:
                with open(filename, 'rb') as f:
                    file = disnake.File(f, filename=filename)
                    embed = disnake.Embed(
                        title=langText.get("LEAVE_TITLE").format(userName=member.display_name),
                        description=langText.get("LEAVE_TEXT").format(userMention=member.mention, usersCount=len(member.guild.members)),
                        color=disnake.Color.brand_red()
                        )
                    embed.set_image(url=f"attachment://{filename}")
                    msg = await leave_channel.send(file=file, embed=embed)
                    await msg.add_reaction("👋")
            try:
                os.remove(filename)
            except:
                pass

def setup(bot):
    bot.add_cog(LeaveMessageUtils(bot))