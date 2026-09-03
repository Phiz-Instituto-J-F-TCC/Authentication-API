-- Migração incremental para bancos que já possuem Token_Autenticacao.
-- Não reaproveita números de telefone legados como Phiz ID.

BEGIN;

ALTER TABLE "Aluno"
ADD COLUMN IF NOT EXISTS "phiz_id" VARCHAR(255);

ALTER TABLE "Token_Autenticacao"
ADD COLUMN IF NOT EXISTS "phiz_id" VARCHAR(255);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'Token_Autenticacao'
          AND column_name = 'numero_celular'
    ) THEN
        ALTER TABLE "Token_Autenticacao"
        ALTER COLUMN "numero_celular" DROP NOT NULL;
    END IF;
END;
$$;

COMMIT;
