from dotenv import load_dotenv
import os
import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services.vault.models.common import KeyPurpose
from pangea.services.vault.models.symmetric import SymmetricAlgorithm
from pangea.services.vault.vault import Vault
from pangea.utils import str2str_b64
from secrets import token_hex

load_dotenv()
token = os.getenv("PANGEA_TOKEN")
domain = os.getenv("PANGEA_DOMAIN")
config = PangeaConfig(domain=domain, queued_retry_enabled=False)
vault = Vault(os.getenv("PANGEA_TOKEN"), config=config)


def encrypt_info(text, key):
    try:
        name =key

        # Create a symmetric key with the default parameters.
        create_response = vault.symmetric_generate(
            purpose=KeyPurpose.ENCRYPTION,
            algorithm=SymmetricAlgorithm.AES128_CFB,
            name=name,
        )
        assert create_response.result
        key_id = create_response.result.id

        msg = str2str_b64(text)
        print(f"Encrypt text: {text}")
        encrypt_response = vault.encrypt(key_id, msg)
        assert encrypt_response.result
        cipher_text = encrypt_response.result.cipher_text
        print(f"Cipher text: {cipher_text}")
        return cipher_text
    except pe.PangeaAPIException as e:
        print(f"Vault Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")


def decrypt_info(key_id, cipher_text):
    try:
        print("Decrypting...")
        decrypt_response = vault.decrypt(key_id, cipher_text)
        assert decrypt_response.result
        plain_text = decrypt_response.result.plain_text
        return plain_text

    except pe.PangeaAPIException as e:
        print(f"Vault Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
