# Silly Paste

[![Build](https://github.com/winny-/sillypaste/actions/workflows/build.yml/badge.svg)](https://github.com/winny-/sillypaste/actions/workflows/build.yml)

Yet another Django pastebin.  Written for a lab and later improved for casual
use.

See example instance [here](https://paste.winny.tech/).

See the supplemental [developer notes](./notes.org) (todo etc).

## Features

- Upload text with a title.  Users can modify and delete their content.
- Compatibility with text-mode browsers
- Syntax highlighting
- User accounts
- Anonymous accounts can delete/update their own pastes
- A RESTful API
- Management via Django Admin
- Paste expiration via cron job
- Basic search support (See the "All Pastes" page)
- HTML Rendering of Markdown and Org Mode documents.
- Healthchecks

### Health checks

Provided by [django-watchman][django-watchman].  See the following URLs:

| Path                 | Description                      |
|----------------------|----------------------------------|
| `/health/`           | JSON endpoint                    |
| `/health/ping/`      | Get a 200 OK and simple response |
| `/health/dashboard/` | Human readable dashboard         |

[django-watchman]: https://github.com/mwarkentin/django-watchman

## Contributing

### Running Sillypaste

#### Run with Docker

```bash
docker-compose up
```

The database will be a Postgresql database with a named volume that is not
mapped into the host filesystem.

#### Run In place

Code hot-reloading doesn't work in Docker.  You can run sillypaste in place via:

```bash
poetry run python -m sillypaste prepare &&
    poetry run python -m sillypaste runserver
```

It will use a `db.sqlite3` in the project directory.  You can change this by setting up `DATABASE_URL` (see possible forms [here](https://github.com/jazzband/dj-database-url#url-schema)).

## LICENSE

Unlicense.  See [LICENSE](./LICENSE).
