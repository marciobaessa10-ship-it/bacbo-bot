import os
import asyncio
import logging
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import UserAlreadyParticipantError

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

API_ID          = 31922041
API_HASH        = "3f1efb25a51933118b55a0669c593365"
SESSION_STRING  = "1ApWapzMBu0ryG5qXZ8bgQnJk9W3MFqNv_x5e8ZA8JLK6pTooX2mRQcOB6KRK--QRJV1t9s7qSHvSjr7i1fvCE4WNQxKRTvV957uASjZ9SqXS5UZSCjamI0Vgi2w0Q-zrreP2hw7ZWouT3w8e2pITCagey_mNmbTobtIjXHxb365d8Ts0Q5hXiN4WvR4LRlqBk6aYuhPez8QkODjfzLnvdmQVnetI6fUCoQGtl0_ZfRK4Owt5qF6SbXdd0X-k5CBQYmpjdCcOrnJUE4jt0uiWMirtir0DS66J2IrJXrDQmPu2cGQ_3E4_sOZYBaMwm5ZTKIu_pVqwhgcVR2MKIEjpZuYnjDOC07Q="
CANAL_ORIGEM    = "reicassinodados"
LINK_GRUPO      = "1T99mXFDpDFiMzgy"  # hash do link t.me/+1T99mXFDpDFiMzgy
LINK_PLATAFORMA = "https://bantubet.co.ao/affiliates/?btag=2442098"

async def main():
    logger.info("🚀 Robô BacBo Bilionário VIP — A FUNCIONAR!")
    logger.info(f"📡 A monitorizar : @{CANAL_ORIGEM}")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    # Entrar no grupo VIP automaticamente
    try:
        await client(ImportChatInviteRequest(LINK_GRUPO))
        logger.info("✅ Entrou no grupo VIP com sucesso!")
    except UserAlreadyParticipantError:
        logger.info("✅ Já está no grupo VIP!")
    except Exception as e:
        logger.warning(f"⚠️ Aviso ao entrar no grupo: {e}")

    # Obter entidades
    canal = await client.get_entity(CANAL_ORIGEM)
    grupo = await client.get_input_entity(await client.get_entity("t.me/joinchat/" + LINK_GRUPO))
    logger.info(f"✅ Canal: {canal.title}")

    botao = [Button.url("🎰 Clique aqui para jogar ↗️", LINK_PLATAFORMA)]

    @client.on(events.NewMessage(chats=canal))
    async def handler(event):
        msg = event.message
        logger.info("📨 Novo sinal recebido!")
        try:
            if msg.photo:
                await client.send_file(grupo, msg.media, caption=msg.text or "", buttons=botao)
            elif msg.video:
                await client.send_file(grupo, msg.media, caption=msg.text or "", buttons=botao)
            elif msg.text:
                await client.send_message(grupo, msg.text, buttons=botao)
            else:
                await client.forward_messages(grupo, msg)
            logger.info("✅ Sinal enviado para o grupo VIP!")
        except Exception as e:
            logger.error(f"❌ Erro: {e}")

    logger.info("👀 A monitorizar... aguardando sinais!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
