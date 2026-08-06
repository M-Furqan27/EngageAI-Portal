# """
# backend/core/config.py

# Central place jahan se saari environment variables (.env) load hoti hain.
# Har module ki router.py/service.py yahan se settings import karega — 
# kisi module ko seedha os.getenv() call nahi karna chahiye.
# """

# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     # Database
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_NAME: str

#     # JWT Auth
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

#     @property
#     def DATABASE_URL(self) -> str:
#         return (
#             f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
#             f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
#         )

#     class Config:
#         env_file = ".env"
        
        

    
#     # Gmail SMTP
#     GMAIL_SMTP_EMAIL: str
#     GMAIL_SMTP_APP_PASSWORD: str

#     # Google Calendar
#     GOOGLE_CALENDAR_CREDENTIALS_FILE: str
#     GOOGLE_CALENDAR_ID: str

# settings = Settings()


from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)



class Settings(BaseSettings):


    # Database

    DATABASE_URL: str



    # JWT

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080



    # SendGrid

    SENDGRID_API_KEY: str

    SENDGRID_FROM_EMAIL: str



    # Google OAuth

    GOOGLE_CLIENT_ID: str

    GOOGLE_CLIENT_SECRET: str

    GOOGLE_REDIRECT_URI: str



    # Encryption

    TOKEN_ENCRYPTION_KEY: str



    # URLs

    FRONTEND_URL: str

    BACKEND_URL: str



    model_config = SettingsConfigDict(

        env_file=".env",

        extra="ignore"

    )



    # compatibility properties
    # for rep_module code


    @property
    def database_url(self):

        return self.DATABASE_URL



    @property
    def sendgrid_api_key(self):

        return self.SENDGRID_API_KEY



    @property
    def sendgrid_from_email(self):

        return self.SENDGRID_FROM_EMAIL



    @property
    def google_client_id(self):

        return self.GOOGLE_CLIENT_ID



    @property
    def google_client_secret(self):

        return self.GOOGLE_CLIENT_SECRET



    @property
    def google_redirect_uri(self):

        return self.GOOGLE_REDIRECT_URI



    @property
    def token_encryption_key(self):

        return self.TOKEN_ENCRYPTION_KEY



    @property
    def backend_url(self):

        return self.BACKEND_URL



    @property
    def frontend_url(self):

        return self.FRONTEND_URL





settings = Settings()




