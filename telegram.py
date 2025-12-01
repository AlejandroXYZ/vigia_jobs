from dotenv import load_dotenv
from aiogram import Bot
import os
import asyncio

load_dotenv()

Token: str = os.getenv("Token")
id_chat = int(os.getenv("id_chat")) 

async def sender(titulo, url):
    if not Token:
        print("Error en el archivo .env")
    else:
        print("Token Detectado")
    try:
        async with Bot(token=Token) as bot:        
            mensaje = f"Nueva Oferta de Trabajo:\n <b>{titulo}</b>\n <a href='{url}'>Enlace Directo</a>"
            await bot.send_message(chat_id=id_chat,text=mensaje,parse_mode="HTML")
            print("Alerta Enviada")
            await asyncio.sleep(2)
            print("Conexión exitosa")
    except Exception as e:
        print("Error durante la conexión")
        print(f"error: {e}")  
        error_str = str(e)
        if "Unauthorized" in error_str:
            print("👉 PISTA: El Token está mal copiado o fue revocado.")
        elif "Chat not found" in error_str:
            print("👉 PISTA: El Chat ID está mal O no le has dado /start al bot.")
        elif "NetworkError" in error_str or "ConnectTimeout" in error_str:
            print("👉 PISTA: Tu internet (CANTV/Inter) no conecta con Telegram. Necesitas VPN.")
        elif "Bad Request" in error_str:
            print("👉 PISTA: Error de formato en el mensaje.")  
    
