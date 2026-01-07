from flask import Flask, request, render_template_string
import requests
import os
import json

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <title>TXT Football Validator</title>
</head>
<body style="font-family:sans-serif; padding:20px">

<h2>TXT Football Data Validator (AI)</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file" accept=".txt" required>
  <button>Analyze</button>
</form>

{% if records %}
<h3>Valid Records</h3>
<table border="1" cellpadding="8">
<tr>
  <th>Name</th>
  <th>Football Team</th>
  <th>Phone</th>
</tr>
{% for r in records %}
<tr>
  <td>{{ r.name }}</td>
  <td>{{ r.football_team }}</td>
  <td>{{ r.phone }}</td>
</tr>
{% endfor %}
</table>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    records = []

    if request.method == "POST":
        text = request.files["file"].read().decode("utf-8")

        prompt = f"""
Extract ONLY valid records.

A valid record must contain:
- name
- football_team
- phone (Myanmar or international)

Rules:
- Missing field → discard
- Normalize phone to digits only
- Output JSON ONLY

Format:
{{"records":[{{"name":"","football_team":"","phone":""}}]}}

TEXT:
{text}
"""

        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": os.environ["GEMINI_API_KEY"]},
            json={"contents":[{"parts":[{"text":prompt}]}]}
        )

        try:
            raw = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            records = json.loads(raw)["records"]
        except:
            records = []

    return render_template_string(HTML, records=records)

app.run(host="0.0.0.0", port=10000)
