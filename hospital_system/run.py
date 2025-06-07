from app import create_app, db
from app.models import (Patient, Employee, Doctor, Department, Medicine,
                        Prescription, MedicalRecord, PrescriptionDetail, Nurse, Ward,
                        PriceChangeLog)
import click
from flask.cli import with_appcontext

app = create_app()

# 移除 init_db_command 函数
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """初始化数据库表结构."""
#     db.create_all()
#     click.echo('数据库初始化完成.')

# app.cli.add_command(init_db_command)


@click.command('create-test-data')
@with_appcontext
def create_test_data():
    """创建测试数据."""
    # 创建部门
    dept1 = Department(dept_id='D001', dept_name='内科', location='门诊楼一层', phone='1001')
    dept2 = Department(dept_id='D002', dept_name='外科', location='门诊楼二层', phone='1002')
    dept3 = Department(dept_id='D003', dept_name='儿科', location='门诊楼一层', phone='1003')

    # 创建员工
    emp1 = Employee(emp_id='E001', name='张医生', gender='M', title='主任医师',
                    contact='13500001111', dept_id='D001')
    emp2 = Employee(emp_id='E002', name='李医生', gender='F', title='副主任医师',
                    contact='13500002222', dept_id='D002')
    emp3 = Employee(emp_id='E003', name='王护士', gender='F', title='主管护士',
                    contact='13500003333', dept_id='D001')

    # 创建医生信息
    doc1 = Doctor(emp_id='E001', specialty='心血管内科', license_number='DOC20210001')
    doc2 = Doctor(emp_id='E002', specialty='普外科', license_number='DOC20210002')

    # 创建药品信息
    med1 = Medicine(medicine_id='M001', name='阿司匹林', specification='100mg*30片',
                    manufacturer='国药集团', price=15.50, stock_quantity=100)
    med2 = Medicine(medicine_id='M002', name='布洛芬', specification='0.2g*10片',
                    manufacturer='白云山制药', price=12.80, stock_quantity=150)
    med3 = Medicine(medicine_id='M003', name='青霉素注射液', specification='80万u/支',
                    manufacturer='华北制药', price=35.00, stock_quantity=80)

    # 创建患者信息
    pat1 = Patient(patient_id='P001', name='刘患者', gender='M', contact='13900001111',
                   insurance_number='INS20210001')
    pat2 = Patient(patient_id='P002', name='陈患者', gender='F', contact='13900002222',
                   insurance_number='INS20210002')

    db.session.add_all([dept1, dept2, dept3, emp1, emp2, emp3, doc1, doc2,
                        med1, med2, med3, pat1, pat2])
    db.session.commit()

    click.echo('测试数据创建完成.')


app.cli.add_command(create_test_data)


@app.shell_context_processor
def make_shell_context():
    """为Flask shell设置上下文."""
    return {
        'db': db,
        'Patient': Patient,
        'Employee': Employee,
        'Doctor': Doctor,
        'Department': Department,
        'Medicine': Medicine,
        'Prescription': Prescription,
        'MedicalRecord': MedicalRecord,
        'PrescriptionDetail': PrescriptionDetail
    }


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()  # 首次运行时创建所有数据库表 - 移除此行
        pass

    app.run(debug=True)  # 以调试模式运行应用