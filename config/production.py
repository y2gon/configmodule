from config.default import *

#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'android_login.db'))
from config.default import *

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='dbmasteruser',
    pw='[Un1UYRrS$fsRNT!F(x30#%g.mUCEx&U',
    url='ls-846c4623a449184c6b65a8d6bb58be75a0eb1e6f.cq29lywrlzdq.ap-northeast-2.rds.amazonaws.com',
    db='flask_pybo'
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xe9b"\xa8\rd\x07\xb3\xa0\x7f\x1b\xb2\xeav:\x13'

