from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# 定义了医院信息管理系统的所有数据模型，使用SQLAlchemy ORM将Python类映射到数据库表
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
# id：自增主键，整数类型
# username：用户名，64字符，唯一索引
# email：邮箱，120字符，唯一索引
# password_hash：密码哈希值，不存储明文密码

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    birth_date = db.Column(db.Date)
    contact = db.Column(db.String(20))
    address = db.Column(db.String(100))
    insurance_number = db.Column(db.String(30))

    medical_records = db.relationship('MedicalRecord', backref='patient', lazy='dynamic')
    # 一对多关系：一个患者可以有多条医疗记录
    def __repr__(self):
        return f'<Patient {self.name}>'
# patient_id：患者ID，业务主键
# name：姓名，必填字段
# gender：性别，单字符（M/F）
# birth_date：出生日期，Date类型
# insurance_number：医保号，重要的医疗保险信息

class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.String(10), primary_key=True)
    dept_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    manager_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'))

    employees = db.relationship('Employee', backref='department', lazy='dynamic', foreign_keys='Employee.dept_id')
    wards = db.relationship('Ward', backref='department', lazy='dynamic')
    # 多重关系与其他表的一对多关系
    def __repr__(self):
        return f'<Department {self.dept_name}>'

# manager_id：外键，指向员工表的科室主任
# 形成了科室与员工之间的循环引用关系
class Employee(db.Model):
    __tablename__ = 'employee'
    emp_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    birth_date = db.Column(db.Date)
    contact = db.Column(db.String(20))
    title = db.Column(db.String(30))
    hire_date = db.Column(db.Date)
    dept_id = db.Column(db.String(10), db.ForeignKey('department.dept_id'))

    managed_dept = db.relationship('Department', backref='manager', uselist=False, foreign_keys=[Department.manager_id])
    doctor_info = db.relationship('Doctor', backref='employee', uselist=False)
    nurse_info = db.relationship('Nurse', backref='employee', uselist=False)
    # managed_dept：一对一，员工可能管理的科室
    # doctor_info：一对一，员工的医生信息（如果是医生）
    # nurse_info：一对一，员工的护士信息（如果是护士）
    # uselist = False：表示一对一关系
    def __repr__(self):
        return f'<Employee {self.name}>'
# title：职称（如主任医师、副主任医师）
#  hire_date：入职日期，用于计算工龄
#  dept_id：所属科室外键

class Doctor(db.Model):
    __tablename__ = 'doctor'
    emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'), primary_key=True)
    specialty = db.Column(db.String(50))
    license_number = db.Column(db.String(30), unique=True)

    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy='dynamic')
    prescriptions = db.relationship('Prescription', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return f'<Doctor {self.emp_id}>'

# 主键继承：使用员工ID作为主键
# 一对一关系：与员工表形成继承关系
# 专业信息：医生特有的专业领域和执业证号
class Nurse(db.Model):
    __tablename__ = 'nurse'
    emp_id = db.Column(db.String(20), db.ForeignKey('employee.emp_id'), primary_key=True)
    nursing_level = db.Column(db.String(20))

    def __repr__(self):
        return f'<Nurse {self.emp_id}>'

# 护士信息相对简单，主要是护理级别
# 同样采用继承设计模式
class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicine_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specification = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    price = db.Column(db.DECIMAL(10, 2))
    stock_quantity = db.Column(db.Integer)

    prescription_details = db.relationship('PrescriptionDetail', backref='medicine', lazy='dynamic')

    def __repr__(self):
        return f'<Medicine {self.name}>'


class Ward(db.Model):
    __tablename__ = 'ward'
    ward_id = db.Column(db.String(10), primary_key=True)
    ward_type = db.Column(db.String(20))
    bed_count = db.Column(db.Integer)
    available_beds = db.Column(db.Integer)
    dept_id = db.Column(db.String(10), db.ForeignKey('department.dept_id'))

    def __repr__(self):
        return f'<Ward {self.ward_id}>'


class Prescription(db.Model):
    __tablename__ = 'prescription'
    prescription_id = db.Column(db.String(20), primary_key=True)
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctor.emp_id'))
    issue_time = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.DECIMAL(10, 2))

    medical_record = db.relationship('MedicalRecord', backref='prescription', uselist=False)
    details = db.relationship('PrescriptionDetail', backref='prescription', lazy='dynamic',
                              cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Prescription {self.prescription_id}>'


class MedicalRecord(db.Model):
    __tablename__ = 'medical_record'
    record_id = db.Column(db.String(20), primary_key=True)
    patient_id = db.Column(db.String(20), db.ForeignKey('patient.patient_id'))
    doctor_id = db.Column(db.String(20), db.ForeignKey('doctor.emp_id'))
    visit_time = db.Column(db.DateTime, default=datetime.now)
    diagnosis = db.Column(db.String(200))
    prescription_id = db.Column(db.String(20), db.ForeignKey('prescription.prescription_id'))

    def __repr__(self):
        return f'<MedicalRecord {self.record_id}>'
# 连接患者、医生、处方的中心表
# 记录完整的就诊信息
# diagnosis：诊断结果，核心医疗信息

class PrescriptionDetail(db.Model):
    __tablename__ = 'prescription_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prescription_id = db.Column(db.String(20), db.ForeignKey('prescription.prescription_id'))
    medicine_id = db.Column(db.String(20), db.ForeignKey('medicine.medicine_id'))
    quantity = db.Column(db.Integer)
    usage = db.Column(db.String(100))

    def __repr__(self):
        return f'<PrescriptionDetail {self.id}>'


class PriceChangeLog(db.Model):
    __tablename__ = 'price_change_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medicine_id = db.Column(db.String(20), db.ForeignKey('medicine.medicine_id'))
    old_price = db.Column(db.DECIMAL(10, 2))
    new_price = db.Column(db.DECIMAL(10, 2))
    change_date = db.Column(db.DateTime, default=datetime.now)

    medicine = db.relationship('Medicine')

    def __repr__(self):
        return f'<PriceChangeLog {self.id}>'

# 记录药品价格变更历史
# 支持价格追溯和合规审计
# 可用于价格趋势分析