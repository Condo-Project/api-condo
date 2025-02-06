import pyotp
import time

from core.config import settings

class OTPService:
    """Classe para fornecer funcionalidades relacionadas a códigos OTP."""

    def __init__(self, secret_key:str):
        """
        Inicializa a instância da classe OTPService.

        Args:
            secret_key (str): A chave secreta usada para gerar códigos OTP.
        """
        self.totp = pyotp.TOTP(secret_key, interval=300, digits=5)
    

    def generate_secret_key(self)->str:
        """
        Gera uma chave privada.

        Returns:
            str: Chave Secreta gerada.
        """
        return pyotp.random_base32()

    def generate_code(self, secret_key:str=None) -> str:
        """
        Gera um código OTP.

        Args:
            secret_key(OPTIONAL[str]): 

        Returns:
            str: O código OTP gerado.
        """
        if not secret_key:
            return self.totp.now() # => '492039'
        return pyotp.TOTP(secret_key, interval=300, digits=5).now()

    def verify_code(self, code:str, secret_key:str=None) -> bool:
        """
        Verifica se um código OTP é válido.

        Args:
            code (str): O código OTP a ser verificado.
            secret_key(OPTIONAL[str]): 

        Returns:
            bool: True se o código for válido, False caso contrário.
        """
        if not secret_key:
            return self.totp.verify(code)
        return pyotp.TOTP(secret_key, interval=300, digits=5).verify(code, valid_window=1)

# Exemplo de uso
otp_service:OTPService = OTPService(settings.OTP_SECRET_KEY)
