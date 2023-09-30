import disnake
from disnake.ext import commands
import finnhub
import io
import matplotlib.pyplot as plt
from utils import error  # Importer la fonction d'erreur personnalisée

# Initialiser la clé API Finnhub
finnhub_client = finnhub.Client(api_key="")

class TradeViewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="tradeview", description="Get stock price information from Finnhub.")
    async def tradeview(self, ctx, choice: str):
        try:
            # Obtenir les données d'historique des prix à partir de l'API Finnhub
            res = finnhub_client.stock_candles(choice, 'D', 30, 0)
            
            if res['s'] == 'no_data':
                await ctx.send(f"No data found for {choice}.")
                return
            
            # Traitement des données pour créer un graphique
            # Assurez-vous de traiter les données d'historique des prix en conséquence
            
            # Créer un graphique
            plt.figure(figsize=(10, 5))
            # Ajoutez ici le code pour tracer le graphique à partir des données
            
            # Convertir le graphique en une image
            image_stream = io.BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()
            image_stream.seek(0)
            
            embed = disnake.Embed(
                title=f"Price Chart for {choice}",
                color=disnake.Color.blurple()
            )
            embed.set_image(url="attachment://chart.png")
            embed.set_footer(text="Data from Finnhub")
            
            await ctx.send(file=disnake.File(fp=image_stream, filename="chart.png"), embed=embed)
        
        except Exception as e:
            embed = error.error_embed(e)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TradeViewCog(bot))
