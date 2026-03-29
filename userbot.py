import asyncio
import logging
from telethon import TelegramClient, events
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
SESSION_STRING  = "1ApWapzMBuzJDA1QeuteePvKYxu8m5vRzb4v5RqRhey46V-RywtGTdoO6aVWWD34klG0P5JvCIMkb1VJE5MbXI1IRS_CBHBDnNP_66xFeKdjYEKzP0r7OUgMP_W-9c7TEyWGH42mLLQBCCf8r7BSGGRjMCa7o13WCC_m5ukZAJFhX53L_VVzDGZHoB81f365oEqPeNESOaqCSaRifvje64FkRJBEsV7JhLE-qsW9EvJTvu7pVujpEzRZEgpmmYs_1XJg9ObgDcREIG-UdXUbjdSFdvMZ7FZ0kfT571vblCl7q3FyPAHSg3CmNltkOARp-3dmm85KxzDWynYCOGQx7Hb9vu50iZ3g="
CANAL_ORIGEM    = "reicassinodados"
INVITE_HASH     = "1T99mXFDpDFiMzgy"
LINK_PLATAFORMA = "https://bantubet.co.ao/affiliates/?btag=2442098"
RODAPE          = f"\n\n🎰 Joga aqui → {LINK_PLATAFORMA}"

async def main():
    logger.info("🚀 Robô BacBo Bilionário VIP — A FUNCIONAR!")
    logger.info(f"📡 A monitorizar : @{CANAL_ORIGEM}")
    logger.info("━" * 50)

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    logger.info("✅ Userbot conectado!")

    grupo = None
    try:
        result = await client(ImportChatInviteRequest(INVITE_HASH))
        grupo = result.chats[0]
        logger.info(f"✅ Entrou no grupo: {grupo.title}")
    except UserAlreadyParticipantError:
        logger.info("✅ Já está no grupo VIP!")
        async for dialog in client.iter_dialogs():
            if "BacBo" in (dialog.name or "") or "Bilion" in (dialog.name or ""):
                grupo = dialog.entity
                logger.info(f"✅ Grupo encontrado: {dialog.name}")
                break
    except Exception as e:
        logger.error(f"❌ Erro ao entrar no grupo: {e}")

    if not grupo:
        logger.error("❌ Grupo não encontrado!")
        async for dialog in client.iter_dialogs():
            logger.info(f"   {dialog.name} | ID: {dialog.id}")
        return

    canal = await client.get_entity(CANAL_ORIGEM)
    logger.info(f"✅ Canal: {canal.title} | Grupo: {grupo.title}")
    logger.info("👀 A monitorizar... aguardando sinais!")

    @client.on(events.NewMessage(chats=canal))
    async def handler(event):
        msg = event.message
        logger.info("📨 Novo sinal recebido!")
        try:
            texto = (msg.text or "") + RODAPE

            if msg.photo:
                await client.send_file(
                    grupo,
                    msg.media,
                    caption=texto,
                    link_preview=False
                )
            elif msg.video:
                await client.send_file(
                    grupo,
                    msg.media,
                    caption=texto,
                    link_preview=False
                )
            elif msg.text:
                await client.send_message(
                    grupo,
                    texto,
                    link_preview=False
                )
            else:
                await client.forward_messages(grupo, msg)

            logger.info("✅ Sinal enviado com sucesso!")
        except Exception as e:
            logger.error(f"❌ Erro ao enviar: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
