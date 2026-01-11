docker compose up -d

docker exec -i canteen_db psql -U canteen_user -d postgres -v ON_ERROR_STOP=1 -c "DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'canteen_user') THEN
    CREATE ROLE canteen_user LOGIN SUPERUSER PASSWORD 'canteen_pass';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'canteen_db') THEN
    CREATE DATABASE canteen_db OWNER canteen_user;
  END IF;
END
\$\$;"