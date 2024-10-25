from components import database, custom_logger
from flask import Flask, request
import requests
import asyncio
import json

CONFIG = json.load(open("config.json", "r"))

app = Flask(__file__)
logger = custom_logger.CustomLogger("HTTP_SERVER")

@app.route("/link/xaman", methods=["POST"])
def link_xaman():
    try:
        data = request.get_json(force=True)
        payload_uuid = data["meta"]["payload_uuidv4"]
    except Exception as e:
        logger.log_error(f"/link/xaman {e}")
        return "Invalid request.", 400

    try:
        payload_get = requests.get(
            f"https://xumm.app/api/v1/platform/payload/{payload_uuid}",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": CONFIG["XAMAN_API_KEY"],
                "X-API-Secret": CONFIG["XAMAN_API_SECRET"]
            }
        ).json()
        
        xrp_address = payload_get["response"]["account"]

        xaman_wallets_db = database.XamanWallets()
        xaman_wallets_db.verify_uuid(uuid=payload_uuid, xrp_address=xrp_address)

    except Exception as e:
        logger.log_error(f"/link/xaman {e}")
        return "An error has occured while trying to verify your request. Please try again.", 400

    return "Hello!", 200

@app.route("/link/twitter")
def link_twitter():
    return "Hello!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444, debug=True)
