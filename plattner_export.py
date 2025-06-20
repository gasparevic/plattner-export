from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def download_xml():
    url = "http://b2b.plattner.rs:44366/export/xml"  # <-- stavi pravu URL adresu
    try:
        r = requests.get(url)
        r.raise_for_status()
        return Response(
            r.content,
            mimetype='application/xml',
            headers={
                "Content-Disposition": "attachment; filename=export.xml"
            }
        )
    except requests.RequestException as e:
        return Response(f"<error>{str(e)}</error>", mimetype='application/xml', status=500)
