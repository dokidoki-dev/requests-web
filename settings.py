# 配置文件
class Config:
    pass


class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
    DEBUG = False
