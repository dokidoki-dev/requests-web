# 配置文件
class Config:
    pass


class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
    DEBUG = False


# 日志记录等级 INFO  DEBUG  不支持设置ERROR，因为ERROR不受控制，自动开启
Log_level = "DEBUG"
