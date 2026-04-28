-- Demo seed for QorA-A PostgreSQL (idempotent)
-- Usage:
--   docker exec -i postgres_db psql -U postgres -d qora_db < scripts/seed_postgres.sql

INSERT INTO users_user
    (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
    ('pbkdf2_sha256$1000000$demo$3Qt6KwZ2s8F6enCM+0OHnQ==$LUA+gS5PkZXhCG6IRx9fYjvAFYB3p7Q4DkZBvI+1f8Q=', NULL, FALSE, 'ana_data', 'Ana', 'Lopez', 'ana_data@qora.local', FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$1000000$demo$3Qt6KwZ2s8F6enCM+0OHnQ==$LUA+gS5PkZXhCG6IRx9fYjvAFYB3p7Q4DkZBvI+1f8Q=', NULL, FALSE, 'carlos_ml', 'Carlos', 'Martin', 'carlos_ml@qora.local', FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$1000000$demo$3Qt6KwZ2s8F6enCM+0OHnQ==$LUA+gS5PkZXhCG6IRx9fYjvAFYB3p7Q4DkZBvI+1f8Q=', NULL, FALSE, 'lucia_bi', 'Lucia', 'Ruiz', 'lucia_bi@qora.local', FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$1000000$demo$3Qt6KwZ2s8F6enCM+0OHnQ==$LUA+gS5PkZXhCG6IRx9fYjvAFYB3p7Q4DkZBvI+1f8Q=', NULL, FALSE, 'mario_dev', 'Mario', 'Perez', 'mario_dev@qora.local', FALSE, TRUE, NOW()),
    ('pbkdf2_sha256$1000000$demo$3Qt6KwZ2s8F6enCM+0OHnQ==$LUA+gS5PkZXhCG6IRx9fYjvAFYB3p7Q4DkZBvI+1f8Q=', NULL, FALSE, 'sofia_ops', 'Sofia', 'Diaz', 'sofia_ops@qora.local', FALSE, TRUE, NOW())
ON CONFLICT (username) DO NOTHING;

INSERT INTO publications_topic (name, description)
VALUES
    ('Data Engineering', 'Pipelines, ingestas y transformaciones de datos.'),
    ('Machine Learning', 'Modelos y entrenamiento en entorno productivo.'),
    ('Business Intelligence', 'Analitica de negocio, KPIs y dashboards.'),
    ('Cloud', 'Operaciones cloud, despliegues y monitorizacion.')
ON CONFLICT (name) DO NOTHING;

INSERT INTO publications_document (content, timestamp, is_approved, title, file, is_public, user_id)
SELECT
    'Buenas practicas para modelado de entidades y relaciones.',
    NOW() - INTERVAL '7 day',
    TRUE,
    'Guia de Modelado de Datos',
    'documents/demo_modelado.pdf',
    TRUE,
    u.id
FROM users_user u
WHERE u.username = 'ana_data'
  AND NOT EXISTS (SELECT 1 FROM publications_document d WHERE d.title = 'Guia de Modelado de Datos');

INSERT INTO publications_document (content, timestamp, is_approved, title, file, is_public, user_id)
SELECT
    'Proceso estandar para entrenar y versionar modelos.',
    NOW() - INTERVAL '5 day',
    TRUE,
    'Playbook de Entrenamiento ML',
    'documents/demo_ml.pdf',
    TRUE,
    u.id
FROM users_user u
WHERE u.username = 'carlos_ml'
  AND NOT EXISTS (SELECT 1 FROM publications_document d WHERE d.title = 'Playbook de Entrenamiento ML');

INSERT INTO publications_document (content, timestamp, is_approved, title, file, is_public, user_id)
SELECT
    'Revisiones para asegurar dashboards confiables y consistentes.',
    NOW() - INTERVAL '3 day',
    TRUE,
    'Checklist de Calidad de Dashboards',
    'documents/demo_bi.pdf',
    FALSE,
    u.id
FROM users_user u
WHERE u.username = 'lucia_bi'
  AND NOT EXISTS (SELECT 1 FROM publications_document d WHERE d.title = 'Checklist de Calidad de Dashboards');

INSERT INTO publications_document (content, timestamp, is_approved, title, file, is_public, user_id)
SELECT
    'Alertas, backups y respuesta a incidencias en produccion.',
    NOW() - INTERVAL '2 day',
    TRUE,
    'Runbook de Operaciones Cloud',
    'documents/demo_cloud.pdf',
    TRUE,
    u.id
FROM users_user u
WHERE u.username = 'sofia_ops'
  AND NOT EXISTS (SELECT 1 FROM publications_document d WHERE d.title = 'Runbook de Operaciones Cloud');
