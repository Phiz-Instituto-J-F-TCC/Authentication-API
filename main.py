from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router


def create_app() -> FastAPI:
    """Factory da aplicação FastAPI."""
    application = FastAPI(
        title="Autenticação Phiz",
        version="1.0.0",
        description="API de autenticação para vinculação de contas Phiz via e-mail.",
    )

    # Registrar rotas
    application.include_router(auth_router)

    return application


app = create_app()
