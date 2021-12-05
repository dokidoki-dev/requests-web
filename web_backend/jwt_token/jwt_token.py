import datetime
import settings
import jwt
from web_backend.logger_text.logger_text import log

logger = log()


class JWT_USER:
    @staticmethod
    def create_token(payload):
        """
        获取用户token，使用jwt方式
        :param payload: payload对象，用户自定义内容
        :param salt: 加密盐
        :return:
        """
        # jwt 生成token方式
        # 第一步：构造headers、payload
        # 第二步：对headers和payload进行base64编码，并且以.来拼接在一起
        # 第三步：对headers和payload拼接的base64字符串进行hs256加密、加盐处理，然后对加密后的加密数据进行base64编码即可
        # 构造header
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        # 设置超时时间，必须设置超时时间
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=settings.Config.jwt_token_timeout)
        # 通过jwt直接处理剩下步骤
        token = jwt.encode(payload=payload, headers=headers, key=settings.Config.jwt_salt, algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token):
        """
        根据token获取payload
        :param token: 前端携带的token
        :return:
        """
        # 解密token步骤
        # 第一步：分割token，以.来分割token为三部分，并且使用base64进行解码
        # 第二步：将没有base64解码分割出来的headers、payload部分重新以 . 来拼接到一起，然后使用HS256以及我们服务端的盐进行加密
        # 第三步：将加密后的数据和分割出来的通过base64解码后的token第三部分进行比对，一致就是正确，不一致就是非法
        try:
            # 从token中获取payload【不校验合法性】(不会校验是否过期)
            # unverified_payload = jwt.decode(token, settings.Config.jwt_salt,, algorithms=['HS256'], verify=False)
            # print(unverified_payload)
            # 从token中获取payload【校验合法性】
            verified_payload = jwt.decode(token, settings.Config.jwt_salt, algorithms=['HS256'], verify=True)
            return verified_payload
        except jwt.exceptions.ExpiredSignatureError:
            logger.info("token已失效")
        except jwt.DecodeError:
            logger.info("token认证失败")
        except jwt.InvalidTokenError:
            logger.info("非法的token")
