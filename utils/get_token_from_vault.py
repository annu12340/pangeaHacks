import os
import pangea.exceptions as pe
from dotenv import load_dotenv
from pangea.config import PangeaConfig
from pangea.services import Vault
from pangea.tools import logger_set_pangea_config

load_dotenv()

def get_token(token_id):
    token = os.getenv("PANGEA_TOKEN")
    domain = os.getenv("PANGEA_DOMAIN")
    config = PangeaConfig(domain=domain, queued_retry_enabled=False)
    vault = Vault(token, config=config)
    response = vault.get(id=token_id)
    return response.result.current_version.secret
