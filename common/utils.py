"""
UTILS
"""

import re


def is_email(dado):
    """
    Verifica se é e-mail ou não
    """
    # Expressões regulares para verificar se é um número de telefone ou e-mail
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    # Verifica se o dado corresponde ao padrão de e-mail
    if re.match(email_pattern, dado):
        return True

    return False
