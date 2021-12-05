# 配置文件
class Config:
    # 设置jwt加密盐
    jwt_salt = "jzsdk!@'.,/390se8wq28~%$#*abvvcgfm,jkjk*()&*%$djks__+_=-=dskl?><Llskla[]ksoasap134w9w30"
    jwt_token_timeout = 24   # 小时制
    cookies_timeout = 86400  # 单位秒


class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
    DEBUG = False


# 日志记录等级 INFO  DEBUG  不支持设置ERROR，因为ERROR不受控制，自动开启
Log_level = "DEBUG"
