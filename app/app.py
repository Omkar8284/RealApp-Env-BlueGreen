from flask import Flask
import os

app = Flask(__name__)

ENV_COLOR = os.getenv("ENV_COLOR", "BLUE")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route("/")
def index():
    color = ENV_COLOR.upper()
    version = APP_VERSION
    return f"""
    <html>
      <head><title>{color} - {version}</title></head>
      <body style="font-family:Arial,Helvetica,sans-serif;">
        <h1 style="color:{'blue' if color=='BLUE' else 'green'}">
          {color} VERSION - Deployed via Blue/Green (v{version})
        </h1>
        <p>Container: {os.getenv('HOSTNAME', 'unknown')}</p>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

