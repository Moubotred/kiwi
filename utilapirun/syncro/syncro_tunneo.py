from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import httpx
import asyncio

def waifus(tipo:str,categotia:str):
    url = f"https://api.waifu.pics/{tipo}/{categotia}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        imagen_waifu =  data['url']
        image_response = requests.get(imagen_waifu, timeout=10)
        return image_response

    if response.status_code != 200:
        return None

def animacion(imagen_base,imagen_superposicion,altura):

    posicion = {
        '_resize':[400, 700],
        '_posicion':[1090, 760],
        '_resize_anime':[400, 330],
        '_posicion_anime':[1120,60],
        } if altura == 1653 else {
        '_resize':[480,470],
        '_posicion':[108,945],

        '_resize_anime':[370,330],
        '_posicion_anime':[100,5],

        }

    # Crear la superposición (puede ser un rectángulo transparente con texto)
    overlay = Image.new("RGBA", imagen_base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # waifu = waifus(tipo='sfw',categotia='neko')
    logo = Image.open(BytesIO(imagen_superposicion.content)).convert("RGBA")
    logo = logo.resize((posicion['_resize'][0],posicion['_resize'][1]))  # Redimensionar si es necesario
    overlay.paste(logo, (posicion['_posicion'][0],posicion['_posicion'][1]), logo)  # Pegar con transparencia

    return overlay

async def lolis(suministro):    

    # Abrir la imagen b ase
    base = Image.open(f"{suministro}.png").convert("RGBA")

    altura,ancho = base.size

    async with httpx.AsyncClient() as client:
        tasks = [
            client.get("https://raw.githubusercontent.com/Moubotred/Noman/refs/heads/main/fracazado.png"),
            client.get(f"https://api.waifu.pics/sfw/neko")
        ]

        responses = await asyncio.gather(*[task for task in tasks])
        url = responses[1].json()['url']
        waifu_response = await client.get(url)

        fracazado = responses[0]
        imagen_fracazado = animacion(imagen_base = base, imagen_superposicion = fracazado ,altura = altura)

        waifu_anime = waifu_response
        imagen_waifu = animacion(imagen_base = base, imagen_superposicion = waifu_anime ,altura = altura)

        # Combinar imágenes
        combined = Image.alpha_composite(base, imagen_fracazado)
        final_image = Image.alpha_composite(combined, imagen_waifu)

        # Guardar el resultado
        final_image.save(f"{suministro}.png", format="PNG")

def recibo_anime(suministro):
    # Abrir la imagen base
    base_image = Image.open(f"{suministro}.png").convert("RGBA")

    altura,ancho = base_image.size

    posicion = {
        '_resize':[400, 700],
        '_posicion':[1090, 760],
        '_resize_anime':[400, 330],
        '_posicion_anime':[1120,60],
        } if altura == 1653 else {
        '_resize':[480,470],
        '_posicion':[108,945],

        '_resize_anime':[370,330],
        '_posicion_anime':[100,5],

        }

    # Crear la superposición (puede ser un rectángulo transparente con texto)
    overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    logo_anime = waifus(tipo='sfw',categotia='neko')
    logo = Image.open(BytesIO(logo_anime.content)).convert("RGBA")
    logo = logo.resize((posicion['_resize'][0],posicion['_resize'][1]))  # Redimensionar si es necesario
    overlay.paste(logo, (posicion['_posicion'][0],posicion['_posicion'][1]), logo)  # Pegar con transparencia

    # Crear la superposición (puede ser un rectángulo transparente con texto)
    overlay_oficial = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay_oficial)

    response = requests.get('https://raw.githubusercontent.com/Moubotred/Noman/refs/heads/main/fracazado.png')
    logo = Image.open(BytesIO(response.content)).convert("RGBA")
    logo = logo.resize((posicion['_resize_anime'][0],posicion['_resize_anime'][1]))  # Redimensionar si es necesario
    overlay_oficial.paste(logo, (posicion['_posicion_anime'][0],posicion['_posicion_anime'][1]), logo)  # Pegar con transparencia
    # Combinar imágenes
    combined = Image.alpha_composite(base_image, overlay)
    final_image = Image.alpha_composite(combined, overlay_oficial)
    # Guardar el resultado
    final_image.save(f"{suministro}.png", format="PNG")
