# filepath: d:\桌面\hospital_system\app\__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_login import LoginManager
from flask.cli import with_appcontext
import click
# 应用工厂文件，负责创建和配置Flask应用实例，初始化各种扩展，注册蓝图和命令
# 扩展对象初始化
db = SQLAlchemy()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'main.login'  # 设置登录视图函数
login.login_message = '请先登录以访问此页面。'
# 数据库扩展 (db)
# 全局对象：在应用包级别创建，供所有模块使用
# 延迟初始化：先创建对象，稍后绑定到具体应用实例
# 前端扩展 (bootstrap)
# 样式集成：自动集成Bootstrap CSS和JavaScript
# 模板支持：提供Bootstrap模板宏和组件
# 登录管理器 (login)
# login_view：未登录用户访问受保护页面时的重定向目标
# login_message：中文登录提示信息
# 会话管理：处理用户登录状态和会话

# 应用工厂函数
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    # 注册蓝图
    from app.routes import main
    app.register_blueprint(main)

    # 注册命令
    from migrations import init_db  # 导入 init_db 模块
    app.cli.add_command(init_db.init_db_ext)

    return app
 # 用户加载器
from app.models import User  # 导入 User 模型

@login.user_loader
def load_user(id):
    return User.query.get(int(id))