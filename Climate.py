import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

# Define thresholds for low, normal, and high carbon footprint, 
low_threshold = 5.0
high_threshold = 15.0

# Emission factors 
emission_factors = {
    "driving": 0.000472 * 1000,  # CO2 emissions per mile for average US car (kg/mile)
    "electricity": 0.000283,  # CO2 emissions per kWh for US grid mix (kg/kWh)
    "diet": 2.5,  # Average carbon footprint of food consumption per kg (example value, you can adjust this)
    "public_transportation": 0.000080,  # CO2 emissions per passenger-mile for public transportation (example value)
    "air_travel": 0.250,  # CO2 emissions per passenger-mile for air travel (example value)
    "recycling": -1.0,  # Negative emission factor for recycling (example value, assuming it reduces emissions)
}

# Conversion factors, 
conversion_factors = {
    "driving": 1 / 2.20462,  # Miles per kilometer, 
    "electricity": 1,  # No conversion needed for kWh
    "diet": 1,  # No conversion needed for food consumption
    "public_transportation": 1,  # No conversion needed for passenger-miles
    "air_travel": 1,  # No conversion needed for passenger-miles
    "recycling": 1,  # No conversion needed (negative emission factor is considered)
}

advice = {
    "driving": {
        "High": "Consider carpooling or using public transportation.",
        "Normal": "Use your car responsibly.",
        "Low": "Feel free to use your car as needed."
    },
    "electricity": {
        "High": "Conserve energy by turning off unnecessary appliances.",
        "Normal": "Use electricity wisely.",
        "Low": "No specific advice for electricity usage. So, feel free!"
    },
    "diet": {
        "High": "Opt for a sustainable and balanced diet.",
        "Normal": "Maintain a healthy and balanced diet.",
        "Low": "No specific dietary advice at the moment. So, feel free!"
    },
    "public_transportation": {
        "High": "Use public transportation to reduce carbon footprint.",
        "Normal": "Consider using public transportation when convenient.",
        "Low": "Feel free to use other transportation methods."
    },
    "air_travel": {
        "High": "Minimize air travel to reduce environmental impact.",
        "Normal": "Consider alternative travel methods if possible.",
        "Low": "No specific advice for air travel at the moment. So, feel free!"
    },
    "recycling": {
        "High": "Recycle and dispose of waste responsibly.",
        "Normal": "Continue proper recycling habits.",
        "Low": "No specific advice for recycling at the moment. So, feel free!"
    },
}

def calculate_carbon_footprint(activity, units, emission_factor):
    """
    Calculate the carbon footprint of an activity given its units and emission factor.

    Parameters:
    activity (str): The name of the activity (e.g. "driving", "electricity", "diet", "public_transportation", "air_travel", "recycling")
    units (float): The amount of the activity (e.g. miles driven, kWh of electricity, kg of food, passenger-miles, etc.)
    emission_factor (float): The emission factor for the activity (e.g. CO2 emissions per mile, kWh, kg, or passenger-mile)

    Returns:
    float: The carbon footprint of the activity in metric tons of CO2 equivalent (MTCO2e)
    """

    # Convert units to metric tons
    units_converted = units * conversion_factors[activity]

    # Calculate carbon footprint
    carbon_footprint = units_converted * emission_factor

    return carbon_footprint

bot = commands.Bot(command_prefix='$', intents=intents)

# Function to determine the carbon footprint level
def get_footprint_level(carbon_footprint):
    if carbon_footprint < low_threshold:
        return "Low"
    elif low_threshold <= carbon_footprint <= high_threshold:
        return "Normal"
    else:
        return "High"

@bot.command()
async def carbon(ctx, activity: str, units: float):
    """
    Calculate the carbon footprint of an activity.

    Parameters:
    ctx (Context): The Discord context object.
    activity (str): The name of the activity (e.g. "driving", "electricity", "diet", "public_transportation", "air_travel", "recycling")
    units (float): The amount of the activity (e.g. miles driven, kWh of electricity, kg of food, passenger-miles, etc.)

    Returns:
    The carbon footprint of the activity in metric tons of CO2 equivalent (MTCO2e)
    """

    if activity not in emission_factors:
        await ctx.send("Invalid activity. Please choose from: driving, electricity, diet, public_transportation, air_travel, recycling.")
        return

    carbon_footprint = calculate_carbon_footprint(activity, units, emission_factors[activity])
    level = get_footprint_level(carbon_footprint)
    if activity in advice:
        await ctx.send(f"The result of Carbon footprint of {units} {activity}: {carbon_footprint:.2f} MTCO2e.\nAdvice: {advice[activity][level]}\nLevel: {level}")
    else:
        await ctx.send(f"The result of Carbon footprint of {units} {activity}: {carbon_footprint:.2f} MTCO2e.\n{level}")

bot.run('MTE0MjI5NzA3NjM3NDQzNzg4OQ.GX9BhN.2PcVQRU54avJXYuDxV0oyjDaV-9SoB6JcELi5s')
