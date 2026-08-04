# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

A small Flask-SocketIO multi-room chat app. Login (`/`) collects name/room/PIN via a
Flask-WTF form; `/chat` renders the room UI; real-time messaging happens over a
`/chat` namespace SocketIO connection defined in `chatapp/sockets.py`.

## Architecture

- App factory pattern: `chatapp/__init__.py:create_app()` builds the Flask app and
  initializes the shared `socketio` instance. Don't instantiate `Flask()` or
  `SocketIO()` anywhere else.
- Room membership and message scoping rely entirely on Flask-SocketIO's built-in
  `join_room`/`leave_room`/`emit(..., room=...)` mechanism. There is intentionally
  **no** manually-tracked global list of connected clients — a prior version of this
  app tracked `clients` in a module-level list and broadcast to all of them regardless
  of room, which silently merged every chat room into one. If you touch
  `chatapp/sockets.py`, keep broadcasts scoped with `room=room` and rely on
  `join_room`/`leave_room` for membership, not manual bookkeeping.
- `chatapp/sockets.py` handles both explicit leaves (`left` event, fired by the UI's
  close button / `onunload`) and abrupt disconnects (`disconnect` event) so presence
  notifications fire either way.
- Chat messages are rendered client-side via `appendMessage()` in `templates/chat.html`,
  which builds DOM nodes with `.text()`, not string-concatenated HTML. Don't revert to
  building `<p>` markup by string concatenation with message content — that reintroduces
  a stored-XSS hole (any chat message could contain a `<script>` payload).
- `chatapp/forms.py`'s `LoginForm` binds the PIN validator at `__init__` time (reads
  `current_app.config['CHAT_PIN']`) rather than at class-definition time, because the
  PIN is environment-configurable via `Config.CHAT_PIN`.

## Deployment targets

- Primary/working target: any long-running host (Heroku/Railway/Fly) via the
  `Procfile` (`gunicorn --worker-class eventlet -w 1 wsgi:app`). Single worker only —
  room state is in-process; scaling workers needs a shared message queue
  (Flask-SocketIO's `message_queue=` option), which isn't wired up here.
- `api/index.py` + `vercel.json` exist for Vercel's Python runtime, but only the plain
  HTTP routes work there. Vercel's serverless functions can't hold the persistent
  WebSocket connections or in-process room state SocketIO needs, so real-time chat does
  not function on Vercel. See README's Deployment section before "fixing" this — it's
  a platform constraint, not a bug, unless the SocketIO transport is replaced with a
  hosted pub/sub backend (Ably/Pusher/etc.), which is a real architecture change.

## Working in this repo

- No test suite exists yet. If you add one, prefer Flask's `test_client()` for HTTP
  routes and `flask_socketio.test_client` for socket events.
- After changing `requirements.txt`, reinstall into `.venv` and smoke-test
  `create_app().test_client()` against `/` and `/chat` before considering the change done.
- Static asset CDN `<script>`/`<link>` tags carry `integrity=`/`crossorigin=` SRI
  attributes — keep them in sync (fetch fresh hashes from cdnjs's API) if you bump a
  CDN library version rather than dropping the attributes.
