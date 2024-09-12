import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request,HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth,OAuthError
import models.models as models
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal



app= FastAPI()
templates = Jinja2Templates(directory="templates")


load_dotenv()

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET',None)
GOOGLE_DISCOVERY_URL = os.environ.get('GOOGLE_DISCOVERY_URL', None)

app.add_middleware(SessionMiddleware, secret_key="string")
oauth = OAuth()
oauth.register(
    name = "google",
    server_metadata_url = GOOGLE_DISCOVERY_URL,
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    client_kwargs = {
        'scope': 'email profile openid',
        'redirect_url' : 'https://57fa-197-237-137-76.ngrok-free.app/auth/callback'
    }
)


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(
        name = "home.html",
        context = {"request": request}
    )

@app.get('/login')
async def login(request: Request):
    url = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, url)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/auth/callback')
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        # Exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)

        # Get user info
        user = token.get('userinfo')

        if user:
            # Use a regular context manager for synchronous database operations
            with db.begin():  # Begin a synchronous transaction
                # Check if the user is already registered
                db_user = db.query(models.StudentAccs).filter(models.StudentAccs.email == user['email']).first()
                
                if not db_user:
                    # Register the user if not already registered
                    new_user = models.StudentAccs(
                        studentID=None,  # Or provide an appropriate ID
                        email=user['email'],
                        password=None,  # Handle password as needed
                        isverified=True,  # Set to True as the user is authenticated
                    )
                    db.add(new_user)
                    db.commit()
                
                # Save user info in the session
                request.session['user'] = dict(user)

        return templates.TemplateResponse(
            name='dashboard.html',
            context={'request': request, 'user': dict(user)}
        )

    except OAuthError as e:
        return templates.TemplateResponse(
            name="error.html",
            context={'request': request, 'error': e.error}
        )
    except SQLAlchemyError as e:
        # Handle any database-related errors
        raise HTTPException(status_code=500, detail=str(e))