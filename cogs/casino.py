import disnake
from disnake.ext import commands
import json
import random
import time
import datetime
from utils import error

cooldown_time = 60 * 60 * 2

class CasinoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "data/casino.json"
        self.cooldown_file = "data/cooldown.json"
        self.min_balance = 50
        self.bet_options = {
            "red": "🔴",
            "black": "⚫️",
            "even": "🔵",
            "odd": "🟡"
        }
        self.payouts = {
            "red": 2,
            "black": 2,
            "even": 2,
            "odd": 2
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('========== ⚙️ Casino ⚙️ ==========')
        print('🔩 /balance has been loaded')
        print('🔩 /earn has been loaded')
        print('🔩 /bet has been loaded')
        print('🔩 /dice has been loaded')
        print('🔩 /caster has been loaded')
        print('🔩 /slot has been loaded')
        print()

    @commands.slash_command(name="balance", description="Check your balance")
    async def balance(self, ctx):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
                if not balance:
                    data[user_id] = 0
                    balance = 0

            embed = disnake.Embed(
                title="Balance",
                description=f"Your balance: ``{balance}`` coins",
                color=disnake.Color.blue()
            )
            await ctx.response.defer()
            await ctx.send(embed=embed)

            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="earn", description="Earn coins")
    async def earn(self, ctx):
        try:
            user_id = str(ctx.author.id)
            current_time = int(time.time())

            with open(self.cooldown_file, 'r') as cooldown_file:
                cooldown_data = json.load(cooldown_file)
                if not cooldown_data:
                    cooldown_data = {}

                last_earn_time = cooldown_data.get(user_id, 0)

                if current_time - last_earn_time >= cooldown_time:
                    with open(self.data_file, 'r+') as data_file:
                        try:
                            data = json.load(data_file)
                        except json.JSONDecodeError:
                            data = {}

                        data.setdefault(user_id, 0)

                        earnings = data[user_id] + 100
                        data[user_id] = earnings

                        cooldown_data[user_id] = current_time

                        data_file.seek(0)
                        json.dump(data, data_file, indent=4)

                    with open(self.cooldown_file, 'w') as cooldown_file:
                        cooldown_data[user_id] = current_time
                        json.dump(cooldown_data, cooldown_file, indent=4)

                    embed = disnake.Embed(
                        title="Earn Coins",
                        description=f"You earned 100 coins!\nYour total balance: ``{earnings}`` coins.",
                        color=disnake.Color.green()
                    )
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    remaining_time = cooldown_time - (current_time - last_earn_time)
                    remaining_time_delta = datetime.timedelta(seconds=remaining_time)
                    remaining_time_str = str(remaining_time_delta)

                    embed = disnake.Embed(
                        title="Earn Coins",
                        description=f"You are on cooldown.\nTry again in ``{remaining_time_str}``.",
                        color=disnake.Color.red()
                    )
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="bet", description="Bet coins | x2 or lost")
    async def bet(self, ctx, amount: int):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r+') as file:
                data = json.load(file)
                balance = data.get(user_id, 0)
                if amount <= 0 or amount > balance:
                    embed = disnake.Embed(title="Invalid Bet Amount", color=disnake.Color.red())
                    embed.add_field(name="Error", value="Invalid bet amount!")
                    await ctx.response.send_message(embed=embed)
                    return
                if balance < self.min_balance:
                    embed = disnake.Embed(title="Insufficient Balance", color=disnake.Color.red())
                    embed.add_field(name="Error", value=f"You need at least {self.min_balance} coins to play!")
                    await ctx.response.send_message(embed=embed)
                    return

                # Game logic: Quitte ou Double
                win_chance = 25  # 25% chance of winning, 75% chance of losing
                outcome = random.choices([True, False], weights=[win_chance, 100 - win_chance], k=1)[0]

                if outcome:
                    winnings = amount * 2
                    data[user_id] += winnings
                    embed = disnake.Embed(title="💰 You Won!", color=disnake.Color.green())
                    embed.add_field(name="Outcome", value="Congratulations! You won the bet.", inline=False)
                    embed.add_field(name="Winnings", value=f"You won `{winnings}` coins!", inline=False)
                    await ctx.response.defer()
                    await ctx.send(embed=embed)
                else:
                    data[user_id] -= amount
                    embed = disnake.Embed(title="😢 You Lost", color=disnake.Color.red())
                    embed.add_field(name="Outcome", value="Better luck next time. You lost the bet.")
                    await ctx.response.defer()
                    await ctx.send(embed=embed)

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="dice", description="Play the dice game")
    async def dice(self, ctx, bet: int):
        try:
            user_id = str(ctx.author.id)
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            
            bal = data[user_id]

            if bal < bet:
                embed = disnake.Embed(title="Dice Game", color=disnake.Color.red())
                embed.add_field(name="You cant play !", value=f"You don't have money to play ``{bet}`` coin try with less.", inline=False)
                await ctx.send(embed=embed)
            else:
                dice_emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)

                payout = 0

                if dice1 == dice2:  # Pair
                    payout = bet * dice1

                embed = disnake.Embed(title="Dice Game", color=disnake.Color.blue())
                embed.add_field(name="Dice Roll Result", value=f"{dice_emojis[dice1 - 1]}  {dice_emojis[dice2 - 1]}", inline=False)

                if payout > 0:
                    data[user_id] += payout
                    embed.add_field(name="Result", value=f"You won `{payout}` coin!")
                    embed.color = disnake.Color.green()
                else:
                    data[user_id] -= bet
                    embed.add_field(name="Bet", value=f"`{bet}`")
                    embed.add_field(name="Result", value="You lost your bet.")
                    embed.color = disnake.Color.red()

                with open(self.data_file, 'w') as file:
                    json.dump(data, file, indent=4)

                await ctx.response.defer()
                await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name="caster", description="Play a game of caster")
    async def caster(self, ctx, bet_option: str, bet_amount: int):
        try:
            user_id = str(ctx.author.id)
            bet_option = bet_option.lower()

            if bet_option not in self.bet_options:
                embed = disnake.Embed(
                    title="Caster",
                    description="Invalid bet option.\n\nPlease choose from ``red``, ``black``, ``even``, ``odd``.",
                    color=disnake.Color.red()
                )
                await ctx.response.send_message(embed=embed)
                return

            if bet_amount <= 0:
                embed = disnake.Embed(
                    title="Caster",
                    description="Invalid bet amount.\nPlease enter a positive value.",
                    color=disnake.Color.red()
                )
                await ctx.response.send_message(embed=embed)
                return

            with open(self.data_file, 'r') as file:
                data = json.load(file)

            balance = data.get(user_id, 0)

            if balance < bet_amount:
                embed = disnake.Embed(
                    title="Caster",
                    description="Insufficient balance.\nYou don't have enough coins to place this bet.",
                    color=disnake.Color.red()
                )
                await ctx.response.send_message(embed=embed)
                return

            result = random.choice(list(self.bet_options.keys()))
            payout = self.payouts.get(bet_option, 0)

            if result == bet_option:
                winnings = bet_amount * payout
                balance += winnings
                embed = disnake.Embed(
                    title="Caster",
                    description=f"Congratulations! You won {self.bet_options[result]}\nand **`{winnings}`** coins!",
                    color=disnake.Color.green()
                )
            else:
                balance -= bet_amount
                embed = disnake.Embed(
                    title="Caster",
                    description=f"Sorry, you lost your bet.\nThe caster rolled {self.bet_options[result]}.",
                    color=disnake.Color.red()
                )
            
            await ctx.response.defer()
            await ctx.send(embed=embed)

            data[user_id] = balance

            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

    @commands.slash_command(name='slot', description='Play the slot machine')
    async def slot(self, ctx, bet: int):
        try:
            if bet <= 0:
                embed = disnake.Embed(
                    title="Slot Machine",
                    description="The bet must be greater than zero.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            with open('data/casino.json', 'r') as file:
                data = json.load(file)

            user_id = str(ctx.author.id)
            if user_id not in data:
                embed = disnake.Embed(
                    title="Slot Machine",
                    description="You are not registered in the casino. Use the `/earn` command to sign up.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            balance = data[user_id]
            if balance < bet:
                embed = disnake.Embed(
                    title="Slot Machine",
                    description="Insufficient balance to place the bet.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

            reels = ["🍒", "🍊", "🍋", "🍇", "🔔", "💎", "🍀", "🍎"]  # Reel symbols
            random.shuffle(reels)  # Shuffle the symbols

            result = []
            for _ in range(3):
                symbol = random.choice(reels)  # Select a random symbol for each reel
                result.append(symbol)
            random.shuffle(reels)
            ligne1 = []
            for _ in range(3):
                symbol = random.choice(reels)  # Select a random symbol for each reel
                ligne1.append(symbol)
            ligne2 = []
            for _ in range(3):
                symbol = random.choice(reels)  # Select a random symbol for each reel
                ligne2.append(symbol)
            embed = disnake.Embed(title="Slot Machine", color=disnake.Color.blurple())
            embed.add_field(name="Reels",
                            value=f"| ``{ligne1[0]} | {ligne1[1]} | {ligne1[2]}`` |\n\n"
                                f"**>** **``{result[0]} | {result[1]} | {result[2]}``** **<**\n\n"
                                f"| ``{ligne2[0]} | {ligne2[1]} | {ligne2[2]}`` |",
                            inline=False
                            )

            if result[0] == result[1] == result[2]:
                win_amount = bet * 10  # Win 10 times the bet amount for matching all 3 reels
                balance += win_amount
                embed.add_field(name="Result", value=f"Congratulations! You won ``{win_amount}`` coins.", inline=False)
            else:
                balance -= bet
                embed.add_field(name="Result", value="Sorry! You didn't get a match.", inline=False)

            data[user_id] = balance

            with open('data/casino.json', 'w') as file:
                json.dump(data, file, indent=4)

            embed.add_field(name="Balance", value=f"Remaining balance: ``{balance}`` coins.", inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CasinoCog(bot))
