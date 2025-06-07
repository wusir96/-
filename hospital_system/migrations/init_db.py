import os
import pymysql
from flask import current_app
from flask.cli import with_appcontext
import click
from flask import Flask
from app import db
from app.models import (Patient, Employee, Doctor, Department, Medicine,
                        Prescription, MedicalRecord, PrescriptionDetail, Nurse, Ward,
                        PriceChangeLog, User)
# 数据库初始化模块，负责创建表结构、执行SQL脚本、导入初始数据等完整的数据库初始化工作
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:wusir2004@localhost/hospital_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'wusir2004')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'hospital_system')

def read_sql_file(filename):
    """读取SQL文件内容"""
    file_path = os.path.join(os.path.dirname(__file__), 'sql', filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def execute_sql_script(script, connection):
    """执行SQL脚本"""
    # 处理可能包含多个语句的脚本
    # 注意：处理DELIMITER需要特殊逻辑
    statements = []
    current_statement = ''
    delimiter = ';'

    for line in script.splitlines():
        # 跳过注释和空行
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith('--'):
            continue

        # 处理分隔符更改
        if stripped_line.upper().startswith('DELIMITER'):
            if current_statement:
                statements.append(current_statement)
                current_statement = ''
            delimiter = stripped_line.split()[1]
            continue

        # 累积语句
        current_statement += line + '\n'

        # 检查语句是否结束
        if stripped_line.endswith(delimiter):
            # 移除分隔符
            if delimiter != ';':
                current_statement = current_statement.rsplit(delimiter, 1)[0] + ';'
            statements.append(current_statement)
            current_statement = ''

    # 添加最后一个语句（如果有）
    if current_statement.strip():
        statements.append(current_statement)

    # 执行每个语句
    with connection.cursor() as cursor:
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"ERROR executing: {statement[:100]}...")
                    print(f"Error message: {str(e)}")
                    raise


def init_database(app):
    """初始化数据库对象（触发器、存储过程、视图）"""
    # 使用应用配置连接数据库
    db_config = {
        'host': app.config.get('MYSQL_HOST', 'localhost'),
        'user': app.config.get('MYSQL_USER', 'root'),
        'password': app.config.get('MYSQL_PASSWORD', 'wusir2004'),
        'database': app.config.get('MYSQL_DB', 'hospital_system'),
        'charset': 'utf8mb4'
    }

    connection = pymysql.connect(**db_config)
    try:
        with connection:
            # 执行触发器脚本
            triggers_sql = read_sql_file('triggers.sql')
            execute_sql_script(triggers_sql, connection)
            print("触发器创建成功")

            # 执行存储过程脚本
            procedures_sql = read_sql_file('procedures.sql')
            execute_sql_script(procedures_sql, connection)
            print("存储过程创建成功")

            # 执行视图脚本
            views_sql = read_sql_file('views.sql')
            execute_sql_script(views_sql, connection)
            print("视图创建成功")

            # 执行初始化数据脚本
            init_data_sql = read_sql_file('init_data.sql')
            execute_sql_script(init_data_sql, connection)
            print("初始数据导入成功")

            connection.commit()
    except Exception as e:
        print(f"初始化数据库对象失败: {str(e)}")
        raise

@click.command('init-db-ext')
@with_appcontext
def init_db_ext():
    """初始化数据库对象（触发器、存储过程、视图）"""
    #app = Flask(__name__)
    #app.config.from_object(Config)
    #with app.app_context():
    #    init_database(app)
    db.create_all()
    init_database(current_app)
    print('数据库初始化完成 (包括 SQL 脚本).')

def init_app(app):
    app.cli.add_command(init_db_ext)