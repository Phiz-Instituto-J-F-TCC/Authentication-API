from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Dados necessários para iniciar a confirmação da vinculação."""
    email: str
    phone_number: str


class AuthenticationEmailStatusRequest(BaseModel):
    """Schema para validar se o e-mail pode iniciar a autenticação."""
    email: str