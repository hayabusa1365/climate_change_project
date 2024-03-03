import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

# Emission factors
emission_factors = {
    "driving": 0.000472 * 1000,  # CO2 emissions per mile for average US car (kg/mile)
    "electricity": 0.000283,  # CO2 emissions per kWh for US grid mix (kg/kWh)
}

# Conversion factors
conversion_factors = {
    "driving": 1 / 2.20462,  # Miles per kilometer
    "electricity": 1,  # No conversion needed for kWh
}

advice = {
    "driving": "Don't use ur car",
    "electricity": "Save your electricity power"
}

def calculate_carbon_footprint(activity, units, emission_factor):
    """
    Calculate the carbon footprint of an activity given its units and emission factor.

    Parameters:
    activity (str): The name of the activity (e.g. "driving", "electricity")
    units (float): The amount of the activity (e.g. miles driven, kWh of electricity)
    emission_factor (float): The emission factor for the activity (e.g. CO2 emissions per mile or kWh)

    Returns:
    float: The carbon footprint of the activity in metric tons of CO2 equivalent (MTCO2e)
    """

    # Convert units to metric tons
    units_converted = units * conversion_factors[activity]

    # Calculate carbon footprint
    carbon_footprint = units_converted * emission_factor

    return carbon_footprint

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def carbon(ctx, activity: str, units: float):
    """
    Calculate the carbon footprint of an activity.

    Parameters:
    ctx (Context): The Discord context object.
    activity (str): The name of the activity (e.g. "driving", "electricity")
    units (float): The amount of the activity (e.g. miles driven, kWh of electricity)

    Returns:
    The carbon footprint of the activity in metric tons of CO2 equivalent (MTCO2e)
    """

    if activity not in emission_factors:
        await ctx.send("Invalid activity. Please choose from: driving, electricity.")
        return

    carbon_footprint = calculate_carbon_footprint(activity, units, emission_factors[activity])
    if activity in advice:
        await ctx.send(f"The result of Carbon footprint of {units} {activity}: {carbon_footprint:.2f} MTCO2e.\n{advice[activity]}")
    else:
        await ctx.send(f"The result of Carbon footprint of {units} {activity}: {carbon_footprint:.2f} MTCO2e.")

bot.run('MTE0MjI5NzA3NjM3NDQzNzg4OQ.GOvday.wuPyu6bQaR4LAUgMtTb0UxXU3OF7kQAT316S5g')
