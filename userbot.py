import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

API_ID          = 31922041
API_HASH        = "3f1efb25a51933118b55a0669c593365"
SESSION_STRING  = "1ApWapzMBu4qR7DLMSY-BV4PVHBnoX2ioPhPkZ_i6O0bv1AUoy2tt8iYxnp6moUMt-q_qcE6be_sL4IHtE8f8uM-070nijNFNXqM5SHOHa6xUblwov4fh9YEape1tO5tT2I3MKa4JOYi41MviabJXQ7h10K3OHA9mZCpp_cB1Rw_FsZ-G_pVwgCGH71PVgD6fWKcD2CL6VvLBp6K-eohlvFQTxwoZajckxcHgB0_O5uhxr3QSlqyAJR5F1GBrJFiCN1iu0TSwmFRdwmO74qSYjkx7QIzut_NwM6AYtoNDJ6EYxG6BzLnAwxNiKkJ3tJqQiKeUhRonsFIvLeaxX27gKsFIry0aRAw="
BOT_TOKEN       = "8678289013:AAHW_Dmzi9EP4qfCQq4ow-JViMBFEyfu2Uk"
ID_GRUPO        = "-7797212070"
CANAL_ORIGEM    = "reicassinodados"
LINK_PLATAFORMA = "https://bantubet.co.ao/affiliates/?btag=2442098"

def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Clique aqui para jogar ↗️", url=LINK_PLATAFORMA)]
    ])

async def enviar(bot, texto=None, foto=None, video=None, caption=""):
    try:
        if foto:
            await bot.send_photo(chat_id=ID_GRUPO, photo=foto, caption=caption, reply_markup=build_keyboard())
        elif video:
            await bot.send_video(chat_id=ID_GRUPO, video=video, caption=caption, reply_markup=build_keyboard())
        elif texto:
            await bot.send_message(chat_id=ID_GRUPO, text=texto, reply_markup=build_keyboard())
        logger.info("✅ Sinal enviado para o grupo VIP!")
    except TelegramError as e:
        logger.error(f"❌ Erro: {e}")

async def main():
    logger.info("🚀 Robô BacBo Bilionário VIP — A FUNCIONAR!")
    logger.info(f"📡 A monitorizar : @{CANAL_ORIGEM}")
    logger.info(f"📤 Grupo destino : {ID_GRUPO}")
    logger.info("━" * 50)

    bot = Bot(token=BOT_TOKEN)
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    canal = await client.get_entity(CANAL_ORIGEM)
    logger.info(f"✅ Canal encontrado: {canal.title}")

    @client.on(events.NewMessage(chats=canal))
    async def handler(event):
        msg = event.message
        logger.info("📨 Novo sinal recebido!")
        try:
            if msg.photo:
                foto = await client.download_media(msg.photo, bytes)
                await enviar(bot, foto=foto, caption=msg.text or "")
            elif msg.video:
                video = await client.download_media(msg.video, bytes)
                await enviar(bot, video=video, caption=msg.text or "")
            elif msg.text:
                await enviar(bot, texto=msg.text)
        except Exception as e:
            logger.error(f"❌ Erro ao processar: {e}")

    logger.info("👀 A monitorizar o canal... aguardando sinais!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
