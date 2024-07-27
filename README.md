# Contrast Agent

Web application to help compare and contrast the paint products of various brands popularly used in the hobby of miniature painting, including Citadel, Vallejo, Army Painter, and eventually others, such as Pro Acryl and Two Thin Coats.

> **NOTE:** This is a work in progress and not ready for primetime (like the majority of my non-work-related endeavors).

## Instructions

### Backend

The api can only be run using the `pnpm run dev` command from a terminal _within_ the api directory. Alternatively, you can directly run the run.py file.

The `api` ("source") directory is where all the application code sits. Below briefly explains each folder/file

| Item      | Description                                     |
| --------- | ----------------------------------------------- |
| api       | The API endpoints for the application           |
| crud      | The CRUD operations used within the application |
| schemas   | The schemas used within the application         |
| config.py | Main application configuration                  |
| main.py   | Application                                     |

## Materials

This application is made possible using the following languages, libraries, and tools:

#### Build System

- [Turborepo](https://turbo.build/repo/docs)

#### Frontend

- [Vue 3](https://vuejs.org)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind](https://tailwindcss.com)

#### Backend

- [Python](https://www.python.org)
- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev)
- [SQLAlchemy](https://www.sqlalchemy.org)
- [PostgreSQL](https://www.postgresql.org)
- [Supabase](https://supabase.com/)
