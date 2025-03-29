### Alembic Migrations

> \[!WARNING\]
> To create the tables if you did not create the endpoints, ensure that you import the models in src/app/models/__init__.py. This step is crucial to create the new models.

Then, while in the `src` folder, run Alembic migrations:

```sh
poetry run alembic revision --autogenerate
```

And to apply the migration

```sh
poetry run alembic upgrade head
```
