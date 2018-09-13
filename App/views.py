import uuid
from flask import Blueprint, render_template, request, url_for
from flask_restful import abort
from werkzeug.security import generate_password_hash, check_password_hash
from App.ext import cache
from App.models import User

user_blue = Blueprint("user",__name__)


@user_blue.route("/register/")
def register():
    return render_template("register.html")



@user_blue.route("/handleregister/",methods = ["POST"])
def handle_register():
    # 1.拿到用户输入的数据
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    gender = request.form.get("gender")
    age = request.form.get("age")

    # 2.把数据存到数据库
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.gender = gender
    user.age = age
    user.email = email
    user.tokon = str(uuid.uuid4())

    try:
        user.save()
    except Exception as ex:
        abort(400)

    # 往缓存里写一对键值对
    cache.set(user.tokon,user.id,timeout=60)


    # 3.给注册的邮箱发送一个激活邮件
    # msg = Message(
    #     subject="欢迎注册脸盆网",
    #     recipients=[]
    # )


# 把发送邮件的过程放到后台去执行

    # 创建一个Message对象
    # msg = Message()
    # msg.subject = "欢迎注册脸盆网"
    # msg.recipients = [email]
    # msg.body =
    # 在url_for里面,不认识的参数会自动变成请求参数
    active_url = url_for("user.handle_active",_external=True,tokon=user.tokon)
    # msg.html = render_template("ActivePage.html",username=username,active_url=active_url)
    # # 把Message发出去
    # mail.send(msg)
    from App.celery_util import send_mail


    subject = "欢迎注册脸盆网"
    recipients = [email]
    html = render_template("ActivePage.html", username=username, active_url=active_url)
    send_mail.delay(subject=subject,recipients=recipients,html=html)

    return "恭喜你注册成功"


@user_blue.route("/handleactive/")
def handle_active():
    # 先获取tokon
    tokon = request.args.get("tokon")
    # 根据tokon 获取 cache里的用户id
    id = cache.get(tokon)
    if not id:
        return "链接已失效,请重新获取"

    # 如果id存在  根据id获取当前用户
    user = User.query.get(id)

    if not user:
        return "激活失败,当前用户不存在"
    if user.is_active == True:
        return "当前用户已经激活,请不要重复激活"
    user.is_active = True

    try:
        user.save()
    except Exception as ex:
        return "激活失败,请重新激活"

    return "激活成功"


@user_blue.route("/login/")
def login():
    return render_template("Login.html")


@user_blue.route("/handlelogin/",methods=["POST"])
def handle_login():
    # 获取用户名,密码
    username = request.form.get("username")
    password = request.form.get("pwd")

    # 验证用户名是否存在
    user = User.query.filter_by(username=username).first()
    if not user:
        return "当前用户不存在"
    # 验证密码
    if check_password_hash(user.password,password):
        if not user.is_active:
            return "该帐号未激活,请先激活在登录"
        return "欢迎回来,%s" % user.username

    return "密码错误,请重新输入"