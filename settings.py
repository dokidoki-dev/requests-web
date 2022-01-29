# 配置文件
class Config:
    pass


class Development(Config):
    ENV = 'development'
    DEBUG = True


class Production(Config):
    ENV = 'production'
    DEBUG = False


# 用户自定义配置
class UserConfig:
    cookies_domain = '.dev-web.com'
    cookies_timeout = 86400  # 单位秒
    # 用户认证方式： 1 开启jwt认证   0 关闭jwt认证
    jwt_on = 1
    # 设置jwt加密盐
    jwt_salt = "jzsdk!@'.,/390se8wq28~%$#*abvvcgfm,jkjk*()&*%$djks__+_=-=dskl?><Llskla[]ksoasap134w9w30"
    jwt_token_timeout = 24  # 小时制
    # 日志记录等级 INFO  DEBUG  不支持设置ERROR，因为ERROR不受控制，自动开启
    Log_level = "DEBUG"
