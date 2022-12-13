import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import time
import asyncio
import json
# Bobb3ll1 / Armeijan palvelusaika laskin, TJ-Laskuri.

token = "" # Aseta Discord botin Token tänne.
target_date = datetime(2023, 12, 14) # Määritä palveluksen päättymisen päivä (Muoto: datetime(VVVV, KK, PV))
palveluksen_alku = datetime(2023, 1, 2) # Määritä milloin sinun palveluksen alkamisen päivä on (Muoto: datetime(VVVV, KK, PV))
palvelusaika = 347 # Aseta luku kuinka pitkä sinun armeijan palvelusaika on.
nimi = "Matti Meikäläinen" # Sinun nimi.
palveluspaikka = "Karjalan Prikaatissa" # Palveluspaikkasi taivutettuna sopivasti.
kanava_id = 0 # Kanava jolle haluat viestin tulevan.
viesti_aika = "06:00" # Aika jolloin haluat että viesti lähetetään. (Muoto: XX:XX)

intents = discord.Intents.default()
intents.members=True
client = discord.Client(command_prefix = '!', intents=intents)

# Matikkaa laskien palvelusaikaa.
current_date = datetime.now()
delta = target_date - current_date
days_left = int(delta.days) + 1

days_elapsed = int(days_left) / palvelusaika
percent_complete = 100 - days_elapsed * 100

target_date2 = palveluksen_alku
delta2 = target_date2 - current_date
days_until = int(delta2.days) + 1

# Muodostetaan yhteys Discordiin.
@client.event
async def on_ready():
    print(f'{client.user} | Yhteys muodostettu! {current_date}')
    tj.start()

@tasks.loop(seconds=60)
async def tj():
    aika = time.strftime("%H:%M")
    if aika == f"{viesti_aika}":
        if days_until >= 1:
            channel = client.get_channel(kanava_id)
            desc = f"""
            Hyvää huomenta :smile: Kello on `{viesti_aika}`
            Tänään jäljellä `{days_until}` päivää kunnes {nimi} astuu asepalvelukseen.
            """
            embed = discord.Embed (title = '`😄📅` **TJ Laskuri.**', description = desc)
            embed.set_thumbnail (url = 'https://i.imgur.com/2yjXFdG.jpg')
            await channel.send(embed=embed)
        if days_until == 0:
            channel = client.get_channel(kanava_id)
            desc = f"""
            Hyvää huomenta :smile: Kello on `{viesti_aika}`

            {nimi} astuu TÄNÄÄN palvelukseen {palveluspaikka}
            """
            embed = discord.Embed (title = '`😄📅` **TJ Laskuri.**', description = desc)
            embed.set_thumbnail (url = 'https://i.imgur.com/2yjXFdG.jpg')
            await channel.send(embed=embed)

            filename = f'päiväraha.json'
            entry = {"raha": 5.2, "pvsuoritettu": 1}
            dict = json.dumps(entry)
            with open(filename, "w") as file2:
                await asyncio.sleep (1 / 20)
                file2.write(dict)
        if days_left == 0:
            channel = client.get_channel(kanava_id)
            desc = f"""
            Hyvää huomenta :smile: Kello on `{viesti_aika}`. 🥳
            
            Tänään on erikoinen päivä. On ehkä juhlimisen aihetta, {nimi} pääsee tänään asepalveluksesta reserviin!
            {nimi} on suorittanut {palvelusaika} päivää asepalvelusta ja on **TJ:** `0`!
            """
            embed = discord.Embed (title = '`😄📅` **TJ Laskuri.** 🥳', description = desc)
            embed.set_thumbnail (url = 'https://i.imgur.com/2yjXFdG.jpg')
            await channel.send(embed=embed)
            await client.close()

        if days_until < 0:
            filename = f'päiväraha.json'
            with open(filename, "r") as file1:
                json_object = json.load(file1)
                raha = json_object[f'raha']
                päivät = json_object[f'pvsuoritettu']
            
            if 1 <= int(päivät) and int(päivät) < 165:
                uusiraha = raha + 5.2
            if 166 <= int(päivät) and int(päivät) < 255:
                uusiraha = raha + 8.7
            if 256 <= int(päivät) and int(päivät) < 347:
                uusiraha = raha + 12.1

            uusiraha2 = round(uusiraha,1)
            channel = client.get_channel(kanava_id)
            desc = f"""
            :mega: **Kompaniassa HERÄTYS!** :mega: 
            *Kello on* `{viesti_aika}`.

            **TJ:** `{days_left}`!
            {nimi} on palvellut `{round(percent_complete,1)}`% asepalveluksestaan. (Eli: `{päivät}` päivää.)
            {nimi} on tienannut `{uusiraha2}` Eur päivärahaa yhteensä.
            """
            embed = discord.Embed (title = '`😄📅` **TJ Laskuri.**', description = desc)
            embed.set_thumbnail (url = 'https://i.imgur.com/2yjXFdG.jpg')
            await channel.send(embed=embed)

            uusipäivä = int(päivät) + 1
            
            filename = f'päiväraha.json'
            entry = {"raha": uusiraha2, "pvsuoritettu": uusipäivä}
            dict = json.dumps(entry)
            
            with open(filename, "w") as file1:
                file1.write(dict)
                await asyncio.sleep (1 / 20)

client.run(token)
