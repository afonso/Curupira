from ..database.setup import Challenge
import utils.logging.log as log
import discord

def get_challenges():
    """
    Essa funcao retorna todos os challenges cadastrados no CTF
    """
    try:
        challenges = Challenge.select(
            Challenge.id,
            Challenge.name, 
            Challenge.points, 
            Challenge.category, 
            Challenge.description,
            Challenge.url
            )
        challs = ""
        for challenge in challenges.iterator(): 
            challs += f'''{challenge.name} ({challenge.id}) - {challenge.points} Pontos - {challenge.category}
                          {challenge.description}
                          {challenge.url}
                       ------------------------------------------------------------
                       '''
        return discord.Embed(title="Ranking", description=challs)
    except Exception as err:
        log.err(err)