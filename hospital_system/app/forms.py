from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
# 定义了医院信息管理系统的所有表单类，使用Flask-WTF扩展处理用户输入、数据验证和表单渲染
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
# username：用户名输入框，必填
# password：密码输入框，必填，自动隐藏输入内容
# remember_me：复选框，用于持久化登录状态
# submit：提交按钮

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('password', message='两次密码不一致')]
    )
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已被注册，请选择其他用户名。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已被注册，请使用其他邮箱。')
# 验证规则：
# 用户名：4-64字符长度限制
# 邮箱：必须是有效的邮箱格式
# 密码：最少8个字符
# 重复密码：必须与密码字段一致
class PatientForm(FlaskForm):
    patient_id = StringField('患者ID', validators=[DataRequired(), Length(max=20)])
    name = StringField('姓名', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('性别', choices=[('M', '男'), ('F', '女')])
    birth_date = DateField('出生日期', format='%Y-%m-%d', validators=[Optional()])
    contact = StringField('联系方式', validators=[Length(max=20)])
    address = TextAreaField('地址', validators=[Length(max=100)])
    insurance_number = StringField('医保号', validators=[Length(max=30)])
    submit = SubmitField('提交')
# SelectField：下拉选择框，预定义性别选项
# DateField：日期选择器，指定日期格式
# TextAreaField：多行文本框，适用于地址等长文本
# Optional()：可选字段，允许为空
class EmployeeForm(FlaskForm):
    emp_id = StringField('员工ID', validators=[DataRequired(), Length(max=20)])
    name = StringField('姓名', validators=[DataRequired(), Length(max=50)])
    gender = SelectField('性别', choices=[('M', '男'), ('F', '女')])
    birth_date = DateField('出生日期', format='%Y-%m-%d', validators=[Optional()])
    contact = StringField('联系方式', validators=[Length(max=20)])
    title = StringField('职称', validators=[Length(max=30)])
    hire_date = DateField('入职日期', format='%Y-%m-%d', validators=[Optional()])
    dept_id = StringField('部门ID', validators=[Length(max=10)])
    submit = SubmitField('提交')

class DoctorForm(FlaskForm):
    emp_id = StringField('员工ID', validators=[DataRequired(), Length(max=20)])
    specialty = StringField('专业领域', validators=[Length(max=50)])
    license_number = StringField('执业证号', validators=[Length(max=30)])
    submit = SubmitField('提交')

class DepartmentForm(FlaskForm):
    dept_id = StringField('科室ID', validators=[DataRequired(), Length(max=10)])
    dept_name = StringField('科室名称', validators=[DataRequired(), Length(max=50)])
    location = StringField('位置', validators=[Length(max=50)])
    phone = StringField('电话', validators=[Length(max=15)])
    manager_id = StringField('负责人ID', validators=[Length(max=20)])
    submit = SubmitField('提交')

class MedicineForm(FlaskForm):
    medicine_id = StringField('药品ID', validators=[DataRequired(), Length(max=20)])
    name = StringField('药品名称', validators=[DataRequired(), Length(max=50)])
    specification = StringField('规格', validators=[Length(max=50)])
    manufacturer = StringField('生产厂家', validators=[Length(max=50)])
    price = DecimalField('单价', places=2, validators=[NumberRange(min=0)])
    stock_quantity = IntegerField('库存量', validators=[NumberRange(min=0)])
    submit = SubmitField('提交')
# DecimalField：货币字段，places=2表示保留两位小数
# IntegerField：整数字段，用于库存数量
# NumberRange(min=0)：确保价格和库存不为负数
class PrescriptionForm(FlaskForm):
    prescription_id = StringField('处方ID', validators=[DataRequired(), Length(max=20)])
    doctor_id = StringField('医生ID', validators=[DataRequired(), Length(max=20)])
    total_amount = DecimalField('总金额', places=2, validators=[NumberRange(min=0)])
    submit = SubmitField('提交')

class PrescriptionDetailForm(FlaskForm):
    medicine_id = StringField('药品ID', validators=[DataRequired(), Length(max=20)])
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(min=1)])
    usage = StringField('用法用量', validators=[Length(max=100)])
    submit = SubmitField('添加药品')

class MedicalRecordForm(FlaskForm):
    record_id = StringField('记录ID', validators=[DataRequired(), Length(max=20)])
    patient_id = StringField('患者ID', validators=[DataRequired(), Length(max=20)])
    doctor_id = StringField('医生ID', validators=[DataRequired(), Length(max=20)])
    visit_time = DateField('就诊时间', format='%Y-%m-%d', validators=[Optional()])
    diagnosis = TextAreaField('诊断结果', validators=[Length(max=200)])
    prescription_id = StringField('处方ID', validators=[Length(max=20)])
    submit = SubmitField('提交')
    # patient_id、doctor_id：建立患者和医生的关联
    # diagnosis：使用TextAreaField，允许输入详细的诊断信息
    # prescription_id：可选字段，关联处方信息