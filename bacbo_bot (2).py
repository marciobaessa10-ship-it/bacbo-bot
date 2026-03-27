"""
╔══════════════════════════════════════════════════════════════╗
║           BAC BO SIGNAL BOT - EVOLUTION GAMING              ║
║         Robô de Sinais Automatizado | Railway Ready          ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import time
import logging
import requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

# ─── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── VARIÁVEIS DE AMBIENTE (Railway / .env) ──────────────────────────────────
BOT_TOKEN       = os.getenv("BOT_TOKEN")
ID_GRUPO        = os.getenv("ID_GRUPO")
LINK_PLATAFORMA = os.getenv("LINK_PLATAFORMA", "https://example.com")
API_FEED_URL    = os.getenv("API_FEED_URL")

# ─── VALIDAÇÃO INICIAL ───────────────────────────────────────────────────────
def validate_env() -> None:
    missing = []
    for var, val in {
        "BOT_TOKEN": BOT_TOKEN,
        "ID_GRUPO": ID_GRUPO,
        "API_FEED_URL": API_FEED_URL,
    }.items():
        if not val:
            missing.append(var)
    if missing:
        raise EnvironmentError(
            f"❌ Variáveis de ambiente não configuradas: {', '.join(missing)}\n"
            "Configure-as no Railway antes de iniciar o bot."
        )

# ─── ESTADO GLOBAL ───────────────────────────────────────────────────────────
class BotState:
    def __init__(self):
        self.last_round_id: str | None = None
        self.color_history: list[str] = []   # "PLAYER" | "BANKER" | "TIE"
        self.greens: int = 0
        self.reds: int = 0
        self.consecutive_greens: int = 0
        self.total_signals: int = 0

state = BotState()

# ─── DATA FEED ───────────────────────────────────────────────────────────────
def get_live_data() -> dict | None:
    """
    Busca o resultado mais recente da mesa de Bac Bo via API externa.

    Formato esperado da API (ajuste conforme seu provider):
    {
        "round_id": "XYZ123",
        "winner": "PLAYER" | "BANKER" | "TIE",
        "history": ["PLAYER", "BANKER", "PLAYER", ...]  // opcional
    }
    """
    try:
        response = requests.get(
            API_FEED_URL,
            timeout=5,
            headers={"Accept": "application/json", "User-Agent": "BacBoBot/1.0"},
        )
        response.raise_for_status()
        data = response.json()

        # ── Normalização: adapte os campos conforme sua API ──────────────────
        round_id = str(data.get("round_id") or data.get("id") or data.get("gameId", ""))
        winner_raw = str(
            data.get("winner") or data.get("result") or data.get("outcome", "")
        ).upper()

        # Mapear variações comuns
        winner_map = {
            "PLAYER": "PLAYER", "JOGADOR": "PLAYER", "P": "PLAYER", "BLUE": "PLAYER",
            "BANKER": "BANKER", "BANCA": "BANKER",   "B": "BANKER", "RED": "BANKER",
            "TIE": "TIE",      "EMPATE": "TIE",      "T": "TIE",
        }
        winner = winner_map.get(winner_raw, "UNKNOWN")

        if not round_id or winner == "UNKNOWN":
            logger.warning(f"Resposta inesperada da API: {data}")
            return None

        return {"round_id": round_id, "winner": winner}

    except requests.exceptions.Timeout:
        logger.warning("API Feed: timeout na requisição.")
    except requests.exceptions.ConnectionError:
        logger.warning("API Feed: falha de conexão.")
    except requests.exceptions.HTTPError as e:
        logger.warning(f"API Feed: erro HTTP {e.response.status_code}.")
    except Exception as e:
        logger.error(f"API Feed: erro inesperado → {e}")

    return None

# ─── LÓGICA DE SINAL ─────────────────────────────────────────────────────────
STREAK_TRIGGER = 3   # Quantidade de cores iguais para disparar sinal (anti-red)

def analyze_history(history: list[str]) -> tuple[str | None, str]:
    """
    Filtro Anti-Red: detecta sequência de STREAK_TRIGGER cores iguais
    e sugere a cor oposta (quebra de tendência).

    Retorna: (cor_sugerida | None, motivo)
    """
    if len(history) < STREAK_TRIGGER:
        return None, f"Histórico insuficiente ({len(history)}/{STREAK_TRIGGER})"

    recent = history[-STREAK_TRIGGER:]

    if all(c == "PLAYER" for c in recent):
        return "BANKER", f"Sequência de {STREAK_TRIGGER}x PLAYER → Quebra esperada"

    if all(c == "BANKER" for c in recent):
        return "PLAYER", f"Sequência de {STREAK_TRIGGER}x BANKER → Quebra esperada"

    return None, "Sem padrão claro no momento"

# ─── FORMATAÇÃO DA MENSAGEM ──────────────────────────────────────────────────
def format_signal_message(suggested_color: str) -> str:
    color_label = "🔵 JOGADOR" if suggested_color == "PLAYER" else "🔴 BANCA"

    accuracy = (
        round((state.greens / (state.greens + state.reds)) * 100)
        if (state.greens + state.reds) > 0
        else 100
    )

    msg = (
        f"🟢 ENTRADA CONFIRMADA 🟢\n"
        f"🚀 Entrar na cor: {color_label}\n"
        f"⚔️ Proteger o 🟡\n\n"
        f"🔄 Fazer 2 gales\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Placar 🟢 {state.greens} 🔴 {state.reds}\n"
        f"🎯 Acertamos {accuracy}% das vezes\n"
        f"💰 Estamos com {state.consecutive_greens} Greens seguidos!"
    )
    return msg

def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Clique aqui para jogar ↗️", url=LINK_PLATAFORMA)]
    ])

# ─── ENVIO DO SINAL ──────────────────────────────────────────────────────────
def send_signal(bot: Bot, suggested_color: str) -> None:
    message  = format_signal_message(suggested_color)
    keyboard = build_keyboard()

    try:
        bot.send_message(
            chat_id=ID_GRUPO,
            text=message,
            reply_markup=keyboard,
            parse_mode=None,   # texto puro — preserva todos os emojis
        )
        state.total_signals += 1
        logger.info(f"✅ Sinal #{state.total_signals} enviado → {suggested_color}")
    except TelegramError as e:
        logger.error(f"Falha ao enviar mensagem no Telegram: {e}")

# ─── LOOP PRINCIPAL ──────────────────────────────────────────────────────────
POLL_INTERVAL = 2   # segundos entre consultas

def run_bot() -> None:
    validate_env()
    bot = Bot(token=BOT_TOKEN)

    # Teste de conexão com o Telegram
    me = bot.get_me()
    logger.info(f"🤖 Bot conectado: @{me.username} | Grupo: {ID_GRUPO}")
    logger.info(f"📡 API Feed: {API_FEED_URL}")
    logger.info(f"🔁 Polling a cada {POLL_INTERVAL}s | Gatilho: {STREAK_TRIGGER} iguais")
    logger.info("━" * 60)

    while True:
        try:
            data = get_live_data()

            if data is None:
                time.sleep(POLL_INTERVAL)
                continue

            round_id = data["round_id"]
            winner   = data["winner"]

            # ── Ignorar rodadas já processadas ────────────────────────────────
            if round_id == state.last_round_id:
                time.sleep(POLL_INTERVAL)
                continue

            # ── Nova rodada detectada ─────────────────────────────────────────
            state.last_round_id = round_id
            if winner in ("PLAYER", "BANKER"):
                state.color_history.append(winner)

            # Manter histórico limitado (últimas 50 rodadas)
            if len(state.color_history) > 50:
                state.color_history = state.color_history[-50:]

            logger.info(
                f"🆕 Round {round_id} | Resultado: {winner} | "
                f"Histórico: {'→'.join(state.color_history[-5:])}"
            )

            # ── Filtro Anti-Red (quebra de tendência) ─────────────────────────
            suggested_color, reason = analyze_history(state.color_history)

            if suggested_color:
                logger.info(f"🎯 Sinal gerado → {suggested_color} | Motivo: {reason}")
                send_signal(bot, suggested_color)
            else:
                logger.info(f"⏸️  Aguardando padrão | {reason}")

        except KeyboardInterrupt:
            logger.info("🛑 Bot encerrado pelo usuário.")
            break
        except Exception as e:
            logger.error(f"Erro inesperado no loop: {e}", exc_info=True)

        time.sleep(POLL_INTERVAL)

# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_bot()
