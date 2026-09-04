# JS Pac-Man — Streamlit App

A classic Pac-Man game (HTML5 canvas + JS) embedded inside a Streamlit app.

## Files

```
pacman-streamlit/
├── app.py                     # Streamlit entrypoint (embeds the game via components.html)
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml            # Theme + server config
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

**Controls:** Arrow keys or WASD. Click inside the game canvas first so it has keyboard focus.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo (keep the folder structure as-is; `app.py` must be at the path you point to).
2. Go to https://share.streamlit.io, sign in, and click "New app".
3. Select your repo/branch and set the main file path to `app.py`.
4. Deploy — no extra configuration needed, `requirements.txt` is picked up automatically.

## Deploy elsewhere (Docker/any host)

```bash
docker run -p 8501:8501 -v $(pwd):/app -w /app python:3.11-slim \
  bash -c "pip install -r requirements.txt && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
```

Or on any VM/container service: install `requirements.txt`, then run
`streamlit run app.py --server.port <PORT> --server.address 0.0.0.0`.

## Notes

- The game itself runs entirely client-side (HTML5 canvas + vanilla JS) inside an iframe via `st.components.v1.html` — Streamlit's Python layer just hosts it, so gameplay is smooth and has no server round-trips.
- To customize the maze, ghost behavior, or speed, edit the `map` array or the `updateGhost`/`gameLoop` functions inside the `PACMAN_HTML` string in `app.py`.
