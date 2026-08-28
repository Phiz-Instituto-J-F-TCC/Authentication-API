class PhizIdentityResolutionError(Exception):
    """Erro seguro ao trocar uma credencial temporária pelo Phiz ID."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def resolve_phiz_id(phiz_login_code: str) -> str:
    """Resolve o Phiz ID somente no servidor, sem persistir a credencial temporária."""
    if not isinstance(phiz_login_code, str) or not phiz_login_code.strip():
        raise PhizIdentityResolutionError(422, "Credencial temporária do Phiz inválida.")

    raise PhizIdentityResolutionError(
        501,
        "A integração oficial de identidade do Phiz ainda não está configurada.",
    )
