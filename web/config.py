import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="khoadpgserver.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="pgadmin@khoadpgserver" #TODO: Update value
    POSTGRES_PW="Zxcvb@12"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://khoatdservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xWabE0ONUOOElKEWcwpJWSxvDldYmhaw3jlxkQUkDHM=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'tdangkhoa.itute@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False