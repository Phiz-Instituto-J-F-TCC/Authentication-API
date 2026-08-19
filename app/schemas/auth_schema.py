from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Schema de entrada para o endpoint de autenticação."""
    email: str
    phone_code: str