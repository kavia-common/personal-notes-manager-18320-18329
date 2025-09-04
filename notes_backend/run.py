from app import app

if __name__ == "__main__":
    # Host/port can be controlled via env FLASK_RUN_PORT etc. but here use defaults.
    app.run(host="0.0.0.0", port=5000)
