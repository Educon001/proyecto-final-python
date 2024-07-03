# FastAPI Project

Este es un proyecto basado en FastAPI, contenedor con Docker y con PostgreSQL como base de datos. Este proyecto incluye SQLAlchemy como ORM, Alembic para migraciones, Pytest para pruebas y soporte para JWT, OAuth2 y WebSockets.

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## Clonar el Repositorio

```bash
git clone https://github.com/Educon001/proyecto-final-python.git
cd proyecto-final-python
```

## Uso del archivo `.env`

- En la raíz de tu proyecto, copia el archivo `.env.example` y nómbralo como `.env`.

  ```bash
  cp .env.example .env
  ```

## Construir y Levantar los Servicios con Docker Compose:

- Ejecuta los siguientes comandos para construir las imágenes y levantar los contenedores:
```bash
     docker-compose up -d --build
     docker-compose exec web alembic upgrade head
```

- Deterner y eliminar todos los contenedores
```bash
     docker-compose down
```

- Detener y eliminar todos los contenedores y volúmenes
```bash
     docker-compose down -v
```

## Acceder a la documentación de la API

- Abre tu navegador y accede a la siguiente dirección:
  - http://localhost:8004/