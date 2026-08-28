from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Dados necessários para iniciar a confirmação da vinculação."""
    email: str
    phiz_id: str


class AuthenticationEmailStatusRequest(BaseModel):
    """Schema para validar se o e-mail pode iniciar a autenticação."""
    email: str
