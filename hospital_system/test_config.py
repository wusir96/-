# test_config.py
from config import Config
import pymysql


def test_config():
    print("=== 配置验证 ===")
    print(f"SECRET_KEY: {'已设置' if Config.SECRET_KEY else '未设置'}")
    print(f"数据库URI: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"SQLALCHEMY_TRACK_MODIFICATIONS: {Config.SQLALCHEMY_TRACK_MODIFICATIONS}")
    print("配置文件语法正确！")


def test_db_connection():
    print("\n=== 数据库连接测试 ===")
    try:
        # 解析数据库连接字符串
        uri = Config.SQLALCHEMY_DATABASE_URI
        uri = uri.replace('mysql+pymysql://', '')
        user_pass, host_db = uri.split('@')
        username, password = user_pass.split(':')
        host, database = host_db.split('/')

        # 尝试连接
        conn = pymysql.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        print("数据库连接成功!")
        conn.close()
    except Exception as e:
        print(f"数据库连接失败: {e}")
        print("请检查:")
        print("1. 数据库密码是否正确")
        print("2. MySQL服务是否运行")
        print("3. 数据库'hospital_system'是否已创建")


if __name__ == "__main__":
    test_config()
    test_db_connection()