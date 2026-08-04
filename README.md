# Python Flask Chat Application

A real-time, multi-room chat application built on Flask, Flask-SocketIO, and Flask-WTF.
Users pick a name, a room, and a shared PIN to enter a chatroom; messages are broadcast
live over WebSockets to everyone else in that room.

## Features

- Multiple independent chat rooms (messages are scoped to the room you're in)
- Join/leave presence notifications, including on abrupt disconnect (browser close, tab kill)
- PIN-gated entry (`CHAT_PIN`, defaults to `2468`)
- Messages are rendered as text nodes client-side (no HTML injection from chat input)

## Project layout

```
chatapp/            Flask application package (factory pattern)
  __init__.py        create_app() + SocketIO instance
  config.py           Config from environment variables
  forms.py             LoginForm (name/room/PIN)
  routes.py             HTTP routes: / (login) and /chat
  sockets.py             SocketIO event handlers (joined/message/left/disconnect)
templates/           Jinja templates (index.html, chat.html)
static/              CSS + favicon
wsgi.py              Local/production entrypoint (socketio.run / gunicorn)
api/index.py         Vercel serverless entrypoint (see Deployment below)
```

## Running locally

```bash
python -m venv .venv
.venv/Scripts/activate        # .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python wsgi.py
```

The app runs on `http://localhost:5000` by default.

### Environment variables

| Variable      | Default          | Purpose                                      |
|---------------|------------------|-----------------------------------------------|
| `SECRET_KEY`  | random per process | Flask session signing key. Set this in production so sessions survive restarts/redeploys. |
| `CHAT_PIN`    | `2468`           | PIN required to enter a chatroom.             |
| `FLASK_DEBUG` | `0`              | Set to `1` to enable Flask debug mode locally. |

## Deployment

### Heroku / Railway / Fly.io / any long-running host (recommended)

These platforms run a persistent process, so WebSockets and in-memory room state work
as intended. The included `Procfile` runs:

```
gunicorn --worker-class eventlet -w 1 wsgi:app --log-file=-
```

Note the single worker (`-w 1`): room membership is tracked in-process, so running
multiple workers/dynos would split clients across processes that can't see each
other's rooms without an external message queue (e.g. Redis) configured via
Flask-SocketIO's `message_queue` option.

### Vercel

A `vercel.json` and `api/index.py` are included so the app can be built and served on
Vercel's Python runtime. **This only serves the login page and any plain HTTP routes.**
Vercel's Python functions are stateless and short-lived — they do not support the
persistent WebSocket connections or in-memory room state that real-time chat requires,
so the actual chat functionality will not work there. Use Vercel only if you need the
static/login-facing parts deployed at a Vercel URL; deploy to a long-running host above
for working chat.

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
