from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Schema de entrada para o endpoint de autenticação."""
    email: str
    phone_code: str


class AuthenticationEmailStatusRequest(BaseModel):
    """Schema para validar se o e-mail pode iniciar a autenticação."""
    email: str
