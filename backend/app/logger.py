import logging
import os
from datetime import datetime

# Cria a pasta de logs se não existir
os.makedirs("logs", exist_ok=True)

# Nome do arquivo de log com a data de hoje
log_filename = f"logs/barbearia_{datetime.now().strftime('%Y-%m-%d')}.log"

# Configura o logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # Salva os logs num arquivo
        logging.FileHandler(log_filename, encoding="utf-8"),
        # Também mostra os logs no terminal
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("barbearia")

