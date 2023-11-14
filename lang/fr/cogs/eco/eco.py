import json

import disnake
from disnake.ext import commands

from lang.fr.utils import error


class EconomyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Economy ⚙️ ==========')
        print('🔩 /baltop has been loaded')
        print('🔩 /pay has been loaded')
        print()

    @commands.slash_command(name="baltop", description="Top 10 des utilisateurs les plus riches")
    async def baltop(self, ctx):
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)

            sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
            top_users = sorted_data[:10]

            embed = disnake.Embed(title="💰 Top 10 des plus riches 💰", color=disnake.Color.blurple())
            for idx, (user_id, balance) in enumerate(top_users, start=1):
                user = self.bot.get_user(int(user_id))
                if user:
                    embed.add_field(name=f"{idx}. {user.display_name}", value=f"Solde: `{balance}` pieces", inline=False)
                else:
                    embed.add_field(name=f"{idx}. Utilisateur pas trouver", value=f"Solde: `{balance}` pieces", inline=False)

            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="pay", description="Paye un utilisateur")
    async def pay(self, ctx, amount: int, user: disnake.Member):
        try:
            if amount <= 0:
                embed = disnake.Embed(
                    title="Montant invalide",
                    description="Le montant doit être supérieur à 0.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            if user.bot:
                embed = disnake.Embed(
                    title="Utilisateur invalide",
                    description="Tu ne peux pas payer un bot.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            sender_id = str(ctx.author.id)
            recipient_id = str(user.id)

            with open(self.data_file, 'r') as file:
                data = json.load(file)
                sender_balance = data.get(sender_id, 0)

            if sender_balance < amount:
                embed = disnake.Embed(
                    title="Solde insuffisant",
                    description="Tu n'as pas assez d'argent pour effectuer cette transaction.",
                    color=disnake.Color.red()
                )
                await ctx.response.defer()
                await ctx.send(embed=embed)
                return

            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                sender_balance -= amount
                recipient_balance = data.get(recipient_id, 0)
                recipient_balance += amount

                data[sender_id] = sender_balance
                data[recipient_id] = recipient_balance

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            embed = disnake.Embed(
                title="💸 Transfere réussit 💸",
                description=f"Tu a bien donnée `{amount}` de piece a  {user.mention}.",
                color=disnake.Color.green()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EconomyCommands(bot))
