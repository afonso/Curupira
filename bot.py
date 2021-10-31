import discord

from discord.ext import commands
from utils.config import TOKEN
from utils.commands.rank import get_ranking_with_user
from utils.commands.flag import check_flag
from utils.database.setup import get_challenge_description, init_database
from utils.commands.user import register_user

# Database setup
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html


bot = commands.Bot(command_prefix='$', description="Boitatech CTF")


@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)


@bot.command()
async def ranking(ctx):
    """
    Esse comando pega os top 10 usuários no ranking
    e dá a posição atual da pessoa que chamou o comando.
    """
    await ctx.send(f"{get_ranking_with_user(ctx)}")


@bot.command()
async def solve(ctx, challId=None, flag=None):
    """
    Esse comando inputa uma flag

    :challId = Id da challenge
    :flag = Flag pra dar input
    """
    await ctx.author.create_dm()
    if isinstance(ctx.channel, discord.channel.DMChannel):
        try:
            if challId and flag:
                await ctx.send(check_flag(challId, flag, ctx.author.id))
            else:
                await ctx.author.dm_channel.send("Você precisa mandar uma `challId` e uma `flag`!")
        except Exception as err:
            print(err)
    else:
        await ctx.author.dm_channel.send("Utilize o comando `$solve` aqui!")


@bot.command()
async def get_description(ctx, challId=None):
    """
    Esse comando deve trazer a descricao de uma chall.

    @Params
    :challId => Id da challenge
    """
    print(challId)
    await ctx.send(get_challenge_description(challId))


@bot.command()
async def register(ctx):
    """
    Registra o usuário
    """
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '\N{White Heavy Check Mark}'

    message = await ctx.send("\nGostaria de se registrar no CTF?")
    symbols = ['\N{White Heavy Check Mark}', '\N{Cross Mark}']
    for symbol in symbols:
        await message.add_reaction(symbol)
    await bot.wait_for('reaction_add', timeout=60.0, check=check)
    await ctx.send(register_user(ctx.author.id))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Boitatech CTF'))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))


if __name__ == "__main__":
    init_database()
    bot.run(TOKEN)
