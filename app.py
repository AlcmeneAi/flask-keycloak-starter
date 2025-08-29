import os
from flask import Flask, redirect, url_for, session, jsonify, render_template_string, request
from authlib.integrations.flask_client import OAuth

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "flask-app")
OIDC_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET", "replace-with-secret")
OIDC_ISSUER = os.getenv("OIDC_ISSUER", "http://localhost:8080/realms/demo")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", "http://localhost:5000/callback")

app = Flask(__name__)
app.secret_key = SECRET_KEY

oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id=OIDC_CLIENT_ID,
    client_secret=OIDC_CLIENT_SECRET,
    server_metadata_url=f"{OIDC_ISSUER}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

HOME_TMPL = """
<!doctype html>
<title>Flask + Keycloak</title>
<h1>Flask + Keycloak (OIDC) Demo</h1>
{% if user %}
  <p>Hi, <b>{{ user.get('preferred_username') or user.get('name') }}</b>!</p>
  <p>Email: {{ user.get('email') }}</p>
  <p><a href="{{ url_for('profile') }}">View raw ID token claims</a></p>
  <p><a href="{{ url_for('logout') }}">Logout</a></p>
{% else %}
  <p>You are not logged in.</p>
  <a href="{{ url_for('login') }}">Login with Keycloak</a>
{% endif %}
"""

@app.route("/")
def index():
    user = session.get("user")
    return render_template_string(HOME_TMPL, user=user)

@app.route("/login")
def login():
    # Insecure: use a fixed state for development only
    return oauth.keycloak.authorize_redirect(redirect_uri=OIDC_REDIRECT_URI, state="dev-fixed-state")

@app.route("/callback")
def callback():
    token = oauth.keycloak.authorize_access_token()
    userinfo = token.get("userinfo") or oauth.keycloak.parse_id_token(token)
    session["user"] = userinfo
    session["id_token"] = token.get("id_token")
    return redirect(url_for("index"))

@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return jsonify(user)

@app.route("/logout")
def logout():
    id_token = session.pop("id_token", None)
    session.clear()
    end_session_endpoint = oauth.keycloak.load_server_metadata().get(
        "end_session_endpoint",
        f"{OIDC_ISSUER}/protocol/openid-connect/logout",
    )
    params = {
        "post_logout_redirect_uri": request.host_url.strip('/') + url_for("index"),
    }
    if id_token:
        params["id_token_hint"] = id_token
    from urllib.parse import urlencode
    return redirect(end_session_endpoint + "?" + urlencode(params))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
