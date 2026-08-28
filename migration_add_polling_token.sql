-- Adiciona um identificador opaco para o polling de solicitações existentes.
-- Registros legados permanecem nulos; novas solicitações sempre recebem valor.

ALTER TABLE "Token_Autenticacao"
ADD COLUMN IF NOT EXISTS "polling_token" VARCHAR(255);

CREATE UNIQUE INDEX IF NOT EXISTS "idx_token_autenticacao_polling_token"
ON "Token_Autenticacao" ("polling_token")
WHERE "polling_token" IS NOT NULL;
