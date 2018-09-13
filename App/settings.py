class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123@localhost:3306/flaskday07"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.163.com"  # 发送的服务器地址
    MAIL_DEFAULT_SENDER = "15122250811@163.com"  # 默认发送邮件的邮箱名
    MAIL_USERNAME = "15122250811@163.com"  # 发送邮件的邮箱名
    MAIL_PASSWORD = "54xiaodai"  # 邮件的第三方授权码