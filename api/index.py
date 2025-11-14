from flask import Flask, request, jsonify
import requests
import time
import json
from datetime import datetime

# DO NOT LEAK! CREATORS: HAZEM, L1RSON, AND SCREAMINGCAT.
app = Flask(__name__)

TITLE_ID = "TItleid"  # Set it to the playfab of the game ur modding
BACKEND_URL = "Playfabauthurl"  # playfabauth url of the game ur modding
DISCORD_WEBHOOK_URL = "Webhook"  # Add your Discord webhook URL
APP_ID = "applabid"  # MAKE SURE TO REPLACE WITH THE APPLABS ID OR YOU WONT AUTH PROPERLY******* (heavily recommended if the game is popular)
APP_SCOPED_ID = None  # DONT TOUCH
METASCOPE_API_URL = f"https://www.metascope.org/api/gen?app_id={APP_ID}" # also dont touch

def send_discord_webhook(success, details):
    
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE": # dont touch ts idk why but its kinda broken lol
        return

    timestamp = datetime.utcnow().isoformat()

    if success:
        color = 0x00FF00  # green
        title = "AUTHENTICATION SUCCESS"
        description = "```ansi\n\u001b[1;32m[SUCCESS]\u001b[0m \u001b[1;36mBackend authentication completed successfully\u001b[0m\n```"

        fields = [
            {
                "name": "Session Details",
                "value": f"```ansi\n\u001b[0;33mSessionTicket:\u001b[0m \u001b[0;32m{details.get('SessionTicket', 'N/A')[:50]}...\u001b[0m\n\u001b[0;33mPlayFabId:\u001b[0m \u001b[0;36m{details.get('PlayFabId', 'N/A')}\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Entity Information",
                "value": f"```ansi\n\u001b[0;35mEntityId:\u001b[0m \u001b[0;32m{details.get('EntityId', 'N/A')}\u001b[0m\n\u001b[0;35mEntityType:\u001b[0m \u001b[0;36m{details.get('EntityType', 'N/A')}\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Backend Configuration",
                "value": f"```ansi\n\u001b[0;34mBackend URL:\u001b[0m \u001b[0;37m{BACKEND_URL}\u001b[0m\n\u001b[0;34mTitle ID:\u001b[0m \u001b[0;37m{TITLE_ID}\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Game:",
                "value": f"```ansi\n\u001b[0;33mRetro Tag\u001b[0m\n```",
                "inline": False
            }
        ]
    else:
        color = 0xFF0000  # red
        title = "AUTHENTICATION FAILURE"
        description = "```ansi\n\u001b[1;31m[FAILURE]\u001b[0m \u001b[1;33mBackend authentication failed\u001b[0m\n```"

        error_msg = details.get('error', 'Unknown error')
        status_code = details.get('status', 'N/A')
        exception = details.get('exception', 'N/A')
        backend_details = details.get('details', 'N/A')

        fields = [
            {
                "name": "Error Information",
                "value": f"```ansi\n\u001b[0;31mError:\u001b[0m \u001b[0;33m{error_msg}\u001b[0m\n\u001b[0;31mStatus Code:\u001b[0m \u001b[0;33m{status_code}\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Debug Details",
                "value": f"```ansi\n\u001b[0;35mException:\u001b[0m \u001b[0;37m{exception}\u001b[0m\n\u001b[0;35mBackend Response:\u001b[0m \u001b[0;37m{str(backend_details)[:100]}...\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Backend Configuration",
                "value": f"```ansi\n\u001b[0;34mBackend URL:\u001b[0m \u001b[0;37m{BACKEND_URL}\u001b[0m\n\u001b[0;34mTitle ID:\u001b[0m \u001b[0;37m{TITLE_ID}\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Request Payload",
                "value": f"```ansi\n\u001b[0;36mCustomId:\u001b[0m \u001b[0;32mOCULUS31647312538249274\u001b[0m\n\u001b[0;36mOculusId:\u001b[0m \u001b[0;32m31647312538249274\u001b[0m\n\u001b[0;36mPlatform:\u001b[0m \u001b[0;32mQuest\u001b[0m\n```",
                "inline": False
            },
            {
                "name": "Timestamp",
                "value": f"```ansi\n\u001b[0;33m{timestamp}\u001b[0m\n```",
                "inline": False
            }
        ]

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields,
        "footer": {
            "text": f"PlayFab Authentication Logger | Title: {TITLE_ID}"
        },
        "timestamp": timestamp
    }

    payload = {
        "embeds": [embed]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Discord webhook: {str(e)}")

def validate_nonce(nonce, oculus_id):

    return True

def fetch_uid_and_nonce():

    try:
        print(f"Fetching UID and nonce from: {METASCOPE_API_URL}")
        resp = requests.get(METASCOPE_API_URL, timeout=10)
        
        print(f"Metascope response status: {resp.status_code}")
        print(f"Metascope response headers: {dict(resp.headers)}")
        print(f"Metascope response: {resp.text}")
        
        if resp.status_code != 200:
            print(f"Failed to fetch from metascope: Status {resp.status_code}")
            print(f"Full response text: {resp.text}")
            return None, None
        
        data = resp.json()
        print(f"📥 Parsed JSON data: {data}")
        
        uid = data.get("id")
        nonce = data.get("nonce")
        
        if not uid or not nonce:
            print(f"Missing uid or nonce in metascope response")
            print(f"Available keys in response: {list(data.keys())}")
            return None, None
        
        print(f"Successfully fetched UID: {uid}")
        print(f"Successfully fetched nonce: {nonce[:20]}...")
        return uid, nonce
        
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching from metascope: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        print(f"Response text was: {resp.text}")
        return None, None
    except Exception as e:
        print(f"Unexpected error fetching from metascope: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        return None, None

def update_app_scoped_id(new_uid):

    global APP_SCOPED_ID
    old_value = APP_SCOPED_ID
    APP_SCOPED_ID = new_uid
    print(f"Updated APP_SCOPED_ID from {old_value} to {APP_SCOPED_ID}")

def backend_login():


    uid, nonce = fetch_uid_and_nonce()
    if not uid or not nonce:
        error_details = {"error": "Failed to fetch UID and nonce from metascope", "metascope_url": METASCOPE_API_URL}
        print(f"Backend login aborted: {error_details}")
        return None, error_details
    
    oculus_id = uid
    if not validate_nonce(nonce, oculus_id):
        return None, {"error": "Invalid nonce"}

    app_version = "" # dont touch or remove

    payload = { # MAKE SURE TO CHANGE
        "CustomId": "OCULUS24372190532453834", #leave blank for antiban or if ur logging into a staffs account change it
        "Nonce": nonce,
        "AppId": "9E9F7", # SET THIS TO YOUR TITLE ID ASWELL OR IT WONT WORK
        "AppVersion": app_version,
        "Platform": "Quest",
        "OculusId": uid
    }
    try:
        print(f"Attempting backend login to: {BACKEND_URL} (AppVersion={app_version})")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print(f"Using UID: {uid}")
        print(f"Using nonce: {nonce[:20]}...")

        resp = requests.post(BACKEND_URL, json=payload, timeout=30)

        print(f"Backend response status: {resp.status_code}")
        print(f"Backend response headers: {dict(resp.headers)}")
        print(f"Backend response: {resp.text}")

        if resp.status_code != 200:
            error_details = {
                "error": "Backend login failed",
                "status": resp.status_code,
                "details": resp.text,
                "headers": dict(resp.headers),
                "AppVersionTried": app_version,
                "backend_url": BACKEND_URL
            }
            print(f"Backend login failed with full details: {json.dumps(error_details, indent=2)}")
            return None, error_details

        data = resp.json()
        session_ticket = data.get("SessionTicket") or data.get("data", {}).get("SessionTicket")

        if not session_ticket:
            print(f"No SessionTicket found in response: {json.dumps(data, indent=2)}")
            return None, {"error": "Backend did not return SessionTicket", "data": data, "status": resp.status_code, "AppVersionTried": app_version}

        print(f"Successfully obtained SessionTicket")
        
        update_app_scoped_id(uid)
        
        return session_ticket, data

    except requests.exceptions.Timeout:
        error_details = {"error": "Backend request timed out", "AppVersionTried": app_version, "backend_url": BACKEND_URL}
        print(f"Timeout error: {json.dumps(error_details, indent=2)}")
        return None, error_details
    except requests.exceptions.ConnectionError as e:
        error_details = {"error": "Cannot connect to backend", "backend_url": BACKEND_URL, "exception": str(e)}
        print(f"Connection error: {json.dumps(error_details, indent=2)}")
        return None, error_details
    except Exception as e:
        error_details = {"error": "Request to backend failed", "exception": str(e), "exception_type": type(e).__name__, "AppVersionTried": app_version}
        print(f"Unexpected error: {json.dumps(error_details, indent=2)}")
        return None, error_details

def playfab_post(path, payload, session_ticket):

    headers = {"Content-Type": "application/json", "X-Authorization": session_ticket}
    url = f"https://{TITLE_ID}.playfabapi.com{path}"
    try:
        print(f"PlayFab request to: {url}")
        print(f"PlayFab payload: {json.dumps(payload, indent=2)}")
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"PlayFab response status: {resp.status_code}")
        print(f"PlayFab response: {resp.text}")
        return resp.status_code, resp.json()
    except Exception as e:
        error_text = getattr(resp, "text", "")
        error_status = getattr(resp, "status_code", 500)
        print(f"PlayFab request failed with status {error_status}: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Response text: {error_text}")
        return error_status, {"error": "Request failed", "exception": str(e), "exception_type": type(e).__name__, "status_code": error_status, "text": error_text}

@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():

    print("Authentication endpoint called")

    session_ticket, resp = backend_login()
    if not session_ticket:
        print(f"Authentication failed: {resp}")
        send_discord_webhook(False, resp)
        return jsonify({"error": "Login failed", "details": resp}), 400

    playfab_id = resp.get("PlayFabId") or resp.get("data", {}).get("PlayFabId")
    entity_token = resp.get("EntityToken") or resp.get("data", {}).get("EntityToken", {})
    entity_id = entity_token.get("EntityId") if isinstance(entity_token, dict) else resp.get("EntityId")
    entity_type = entity_token.get("EntityType") if isinstance(entity_token, dict) else resp.get("EntityType")

    result = {
        "SessionTicket": session_ticket,
        "PlayFabId": playfab_id,
        "EntityToken": entity_token,
        "EntityId": entity_id,
        "EntityType": entity_type,
        "UpdatedAppScopedId": APP_SCOPED_ID
    }

    print(f"Authentication successful")
    send_discord_webhook(True, result)
    return jsonify(result), 200

@app.route("/api/PurchaseItemIds", methods=["POST"]) # this doesnt work - hazem
def purchase_item_ids():

    data = request.get_json(silent=True) or {}
    item_ids = data.get("ItemIds", None)
    if isinstance(item_ids, str):
        item_ids = [item_ids]
    if not item_ids and "ItemId" in data:
        item_ids = [data["ItemId"]]
    if not item_ids:
        return jsonify({"error": "No ItemIds provided"}), 400

    catalog_version = data.get("CatalogVersion", "DLC")
    currency_code = data.get("CurrencyCode", "SR")

    session_ticket, login_resp = backend_login()
    if not session_ticket:
        return jsonify({"error": "Login failed", "details": login_resp}), 400

    status, cat_resp = playfab_post("/Client/GetCatalogItems", {"CatalogVersion": catalog_version}, session_ticket)
    if status != 200:
        return jsonify({"error": "Failed to fetch catalog", "details": cat_resp}), status

    catalog = {item["ItemId"]: item for item in cat_resp.get("data", {}).get("Catalog", [])}
    results = []

    for item_id in item_ids:
        item = catalog.get(item_id)
        if not item:
            results.append({"ItemId": item_id, "Status": "NotFound"})
            continue

        price = (item.get("VirtualCurrencyPrices") or {}).get(currency_code)
        if price is None:
            results.append({"ItemId": item_id, "Status": "NoPrice"})
            continue

        payload = {
            "CatalogVersion": catalog_version,
            "ItemId": item_id,
            "VirtualCurrency": currency_code,
            "Price": price
        }

        p_status, p_resp = playfab_post("/Client/PurchaseItem", payload, session_ticket)
        results.append({
            "ItemId": item_id,
            "Price": price,
            "Status": "Purchased" if p_status == 200 else "Failed",
            "Response": p_resp
        })
        time.sleep(0.05)

    return jsonify({
        "CatalogVersion": catalog_version,
        "CurrencyCode": currency_code,
        "TotalProcessed": len(results),
        "Results": results
    }), 200

@app.route("/")
def home():
    return f"ok. logging into {BACKEND_URL} for title id: {TITLE_ID}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
