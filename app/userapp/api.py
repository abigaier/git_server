from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPBasicAuth
from flask import g
from itsdangerous import BadSignature, SignatureExpired

from app.userapp.models import User
from app.utils import class2data

SECRET_KEY = "vhadgvkasbvksdkvbkjsdbvj"

auth = HTTPBasicAuth()
# 查询用户模块
def list_user():
    data = User.all_user()
    result = class2data(data, User.__fields__)
    return result

# 用户登录模块
# 1. 生成token，有效时间为600min
def generate_auth_token(user_id, expiration=36000):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'user_id': user_id})

# 2. 解析token
def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        data = s.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    except BadSignature:
        return None

# 3. 验证token 拦截方法
@auth.verify_password
def verify_password(nickname, password_hash):
    # 先验证token
    user_id = verify_auth_token(nickname)
    # 如果token不存在，验证用户名和密码是否匹配
    if not user_id:
        user = User.get_user(nickname, password_hash)
        user_id = class2data(user, ["nickname"])
        if not user_id:
            return False
    g.user_id = user_id
    return True


# 用户注册模块
def User_reg(nickname, password_hash):
    #校验名字是否重复
    result = User.get_nickname(nickname)
    res = class2data(result, ["nickname"])
    if not res:
        result = User.reg(nickname, password_hash)
        return result
    
    return "用户名重复，注册失败"
