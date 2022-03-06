# Silly Paste

[![Build](https://github.com/winny-/sillypaste/actions/workflows/build.yml/badge.svg)](https://github.com/winny-/sillypaste/actions/workflows/build.yml)

Yet another Django pastebin.  Written for a lab and later improved for casual
use.

See example instance [here](https://sillypaste.herokuapp.com/).

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
- Prometheus exporter for stats

### Health checks

Provided by [django-watchman][django-watchman].  See the following URLs:

| Path                 | Description                      |
|----------------------|----------------------------------|
| `/health/`           | JSON endpoint                    |
| `/health/ping/`      | Get a 200 OK and simple response |
| `/health/dashboard/` | Human readable dashboard         |

[django-watchman]: https://github.com/mwarkentin/django-watchman

## LICENSE

Unlicense.  See [LICENSE](./LICENSE).
