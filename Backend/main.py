# python - example `main.py` that DOES NOT spawn a second reloader when run directly
if __name__ == "__main__":
    import uvicorn
    # set reload=False if you run `python main.py`; use --reload only when running via `uvicorn` CLI
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=False)
