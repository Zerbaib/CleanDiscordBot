import disnake
from disnake.ext import commands
import yfinance as yf
import matplotlib.pyplot as plt
import io
from difflib import get_close_matches
from utils import error

class TradeViewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="tradeview", description="Get stock price information from Yahoo Finance.")
    async def tradeview(self, ctx, choice: str):
        try:
            await ctx.response.defer()
            
            stock = yf.Ticker(choice)
            history = stock.history(period="1mo", interval="1d")
            
            if history.empty:
                # Find closest matches
                stock_symbols = fetch_stock_symbols()  # You need to implement fetch_stock_symbols function
                close_matches = get_close_matches(choice, stock_symbols)
                if close_matches:
                    suggestion_list = "\n".join(close_matches[:3])
                    embed = disnake.Embed(
                        title="Stock Symbol Not Found",
                        description=f"Did you mean: {choice}?\n\nSuggestions:\n{suggestion_list}",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="No Data Found",
                        description=f"No data found for {choice}.",
                        color=disnake.Color.red()
                    )
                    await ctx.send(embed=embed)
                return
            
            current_price = history['Close'][-1]
            last_month_prices = history['Close']
            dates = history.index.date
            
            # Create a simple price chart
            plt.figure(figsize=(10, 5))
            plt.plot(dates, last_month_prices, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title(f"Stock Price for {choice}")
            plt.grid(True)
            
            # Convert the plot to an image
            image_stream = io.BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()
            image_stream.seek(0)
            
            embed = disnake.Embed(
                title=f"Stock Price for {choice}",
                description=f"Current Price: {current_price:.2f} USD",
                color=disnake.Color.blurple()
            )
            embed.set_image(url="attachment://chart.png")
            embed.set_footer(text="Data from Yahoo Finance")
            
            msg = await ctx.send(file=disnake.File(fp=image_stream, filename="chart.png"), embed=embed)
            await ctx.message.delete(delay=5)
            await msg.delete(delay=60)
        
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TradeViewCog(bot))
