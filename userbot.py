import os
import asyncio
import logging
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

API_ID          = 31922041
API_HASH        = "3f1efb25a51933118b55a0669c593365"
SESSION_STRING  = "1ApWapzMBu4qR7DLMSY-BV4PVHBnoX2ioPhPkZ_i6O0bv1AUoy2tt8iYxnp6moUMt-q_qcE6be_sL4IHtE8f8uM-070nijNFNXqM5SHOHa6xUblwov4fh9YEape1tO5tT2I3MKa4JOYi41MviabJXQ7h10K3OHA9mZCpp_cB1Rw_FsZ-G_pVwgCGH71PVgD6fWKcD2CL6VvLBp6K-eohlvFQTxwoZajckxcHgB0_O5uhxr3QSlqyAJR5F1GBrJFiCN1iu0TSwmFRdwmO74qSYjkx7QIzut_NwM6AYtoNDJ6EYxG6BzLnAwxNiKkJ3tJqQiKeUhRonsFIvLeaxX27gKsFIry0aRAw="
CANAL_ORIGEM    = "reicassinodados"
ID_GRUPO        = -1001087968824
LINK_PLATAFORMA = "https://bantubet.co.ao/affiliates/?btag=2442098"

async def main():
    logger.info("🚀 Robô BacBo Bilionário VIP — A FUNCIONAR!")
    logger.info(f"📡 A monitorizar : @{CANAL_ORIGEM}")
    logger.info(f"📤 Grupo destino : {ID_GRUPO}")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    canal = await client.get_entity(CANAL_ORIGEM)
    grupo = await client.get_entity(ID_GRUPO)
    logger.info(f"✅ Canal: {canal.title}")
    logger.info(f"✅ Grupo: {grupo.title}")

    botao = [Button.url("🎰 Clique aqui para jogar ↗️", LINK_PLATAFORMA)]

    @client.on(events.NewMessage(chats=canal))
    async def handler(event):
        msg = event.message
        logger.info("📨 Novo sinal recebido!")
        try:
            if msg.photo:
                await client.send_file(
                    grupo,
                    msg.media,
                    caption=msg.text or "",
                    buttons=botao
                )
            elif msg.video:
                await client.send_file(
                    grupo,
                    msg.media,
                    caption=msg.text or "",
                    buttons=botao
                )
            elif msg.text:
                await client.send_message(
                    grupo,
                    msg.text,
                    buttons=botao
                )
            else:
                await client.forward_messages(grupo, msg)

            logger.info("✅ Sinal enviado para o grupo VIP!")

        except Exception as e:
            logger.error(f"❌ Erro: {e}")

    logger.info("👀 A monitorizar... aguardando sinais!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
