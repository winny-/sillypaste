# Silly Paste

[![Build](https://github.com/winny-/sillypaste/actions/workflows/build.yml/badge.svg)](https://github.com/winny-/sillypaste/actions/workflows/build.yml)

Yet another Django pastebin.  Written for a lab and later improved for casual
use.

See example instance [here](https://sillypaste.herokuapp.com/).

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
- Prometheus exporter for stats

### Health checks

Provided by [django-watchman][django-watchman].  See the following URLs:

| Path                 | Description                      |
| -------------------- | -------------------------------- |
| `/health/`           | JSON endpoint                    |
| `/health/ping/`      | Get a 200 OK and simple response |
| `/health/dashboard/` | Human readable dashboard         |

[django-watchman]: https://github.com/mwarkentin/django-watchman

## LICENSE

Unlicense.  See [LICENSE](./LICENSE).

## develop locally

*requirements:
- python
- (optional if you dont have PostGres installed locally)pg_config(install `libpq-dev` on Debian/Ubuntu; `libpq-devel` on CentOS/Fedora/Cygwin/Babun)
- (on Debian/Ubuntu) - make sure `python3` command is "aliased" to `python`:
    ```bash
    sudo apt-get install python-dev-is-python3
    ```

### install app locally to a python virtual environment

```bash
python -m venv env
source env/bin/activate
pip install -r requirements
python manage.py runserver
```