from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from msal import PublicClientApplication
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.httpx_client import AsyncOAuth2Client


CLIENT_ID = "55bce16e-0390-4316-b8d4-76578a0f27a8"
REDIRECT_URI = "http://localhost:8001/auth/callback"
AUTHORITY = "https://login.microsoftonline.com/7c0c36f5-af83-4c24-8844-9962e0163719"
SCOPE = ["User.Read"]

app = FastAPI(
    title="Xyris Insurance | Powered by Langchain",
    version="1.0.0",
    openapi_url=None,
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="../Frontend/Xyris-Poc/dist/assets", html=True), name="assets")

msal_app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY
)

oauth = OAuth()

oauth.register(
    name='microsoft',
    client_id=CLIENT_ID,
    client_kwargs={
        'scope': 'openid profile',
        'token_endpoint_auth_method': 'none'
    }
)

@app.get("/")
@app.get("/{path:path}")
async def serve_react_app(request: Request, path: str):
    build_path = Path("../Frontend/Xyris-Poc/dist")
    index_html_path = build_path / "index.html"
    if path == "" or path is None:
        index_path = index_html_path
    else:
        index_path = build_path / path

    if index_path.suffix == ".html":
        return FileResponse(index_path, media_type="text/html")
    elif index_path.suffix == "":
        return FileResponse(index_html_path, media_type="text/html")
    elif index_path.suffix == ".svg":
        return FileResponse(index_path, media_type="image/svg+xml")
    elif index_path.suffix == ".png":
        return FileResponse(index_path, media_type="image/png")
    elif index_path.name == "favicon.ico":
        return FileResponse(index_path, media_type="image/x-icon")

    return HTMLResponse(content="React App not found", status_code=404)

@app.get("/auth/login")
async def microsoft_sso_login():
    print("redirect1")
    authorization_url, state = oauth.microsoft.create_authorization_url(
        REDIRECT_URI,
        response_mode='form_post',
        scope='openid profile'
    )
    print("redirec2")
    return RedirectResponse(authorization_url)

@app.post("/auth/callback")
async def microsoft_sso_callback(request: Request):
    token = await oauth.microsoft.authorize_access_token(request)
    userinfo = await oauth.microsoft.parse_id_token(request, token)

    access_token = token['access_token']
    id_token = token['id_token']
    redirect_url = "/Authsuccess?access_token={}&id_token={}".format(access_token, id_token)
    return RedirectResponse(redirect_url)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
