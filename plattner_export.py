from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# --------------------
# KONFIGURACIJA
# --------------------
USERNAME = "igor@motoroom.rs"
PASSWORD = "Igor321."
BASE_URL = "http://b2b.plattner.rs:44366"
PER_PAGE = 100

# --------------------
# POMOĆNE FUNKCIJE
# --------------------
def get_token():
    url = f"{BASE_URL}/Token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def get_all_products(token):
    headers = {"Authorization": f"Bearer {token}"}
    products = []
    page = 0
    while True:
        url = f"{BASE_URL}/api/product/GetAllProduct?Page={page}&perPage={PER_PAGE}"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        batch = r.json().get("Entities", [])
        if not batch:
            break
        products.extend(batch)
        if len(batch) < PER_PAGE:
            break
        page += 1
    return products

def build_xml(products):
    root = ET.Element("Products")
    for p in products:
        product = ET.SubElement(root, "Product")
        for k, v in p.items():
            el = ET.SubElement(product, k)
            el.text = str(v) if v is not None else ""
    return ET.tostring(root, encoding="utf-8", method="xml")

# --------------------
# FLASK RUTA
# --------------------
@app.route("/")
def serve_xml():
    try:
        token = get_token()
        products = get_all_products(token)
        xml_data = build_xml(products)
        return Response(
            xml_data,
            mimetype="application/xml",
            headers={"Content-Disposition": "attachment; filename=products.xml"}
        )
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", mimetype="application/xml")

# --------------------
# START
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
