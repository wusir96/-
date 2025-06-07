from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models import (Patient, Employee, Doctor, Department, Medicine,
                        Prescription, MedicalRecord, PrescriptionDetail, Nurse, Ward,
                        PriceChangeLog)
from app.forms import (PatientForm, EmployeeForm, DoctorForm, DepartmentForm,
                       MedicineForm, PrescriptionForm, PrescriptionDetailForm, MedicalRecordForm)
from sqlalchemy import text
import uuid
from datetime import datetime
from app import db, login
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlparse  # 替换为这行
from sqlalchemy import func  # 添加这行导入
main = Blueprint('main', __name__)
# routes.py 路由文件
# 医院信息管理系统的核心路由控制器，定义了所有的URL路由、视图函数和业务逻辑处理

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':  # 修改这里
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)
#重复登录检查：已登录用户直接跳转首页
# 密码验证：使用安全哈希验证
# 记住我功能：支持持久化登录
# 重定向安全：防止开放重定向攻击
# 错误提示：用户友好的中文错误信息

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录！')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='注册', form=form)


# ===== 首页 =====
@main.route('/')
def index():
    # 统计信息
    patients_count = Patient.query.count()
    employees_count = Employee.query.count()
    medicines_count = Medicine.query.count()
    prescriptions_count = Prescription.query.count()
    departments_count = Department.query.count()

    # 低库存药品
    low_stock_medicines = Medicine.query.filter(Medicine.stock_quantity < 10).all()

    return render_template('index.html',
                           patients_count=patients_count,
                           employees_count=employees_count,
                           medicines_count=medicines_count,
                           prescriptions_count=prescriptions_count,
                           departments_count=departments_count,
                           low_stock_medicines=low_stock_medicines)

# 统计数据：各类实体的总数统计
# 预警信息：库存低于10的药品列表
# 业务概览：为管理决策提供数据支持
# ===== 患者管理 =====
@main.route('/patients')
#@login_required  # 移除这一行
def list_patients():
    patients = Patient.query.all()
    return render_template('patients/list.html', patients=patients)


@main.route('/patients/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            patient_id=form.patient_id.data,
            name=form.name.data,
            gender=form.gender.data,
            birth_date=form.birth_date.data,
            contact=form.contact.data,
            address=form.address.data,
            insurance_number=form.insurance_number.data
        )
        db.session.add(patient)
        try:
            db.session.commit()
            flash('患者添加成功')
            return redirect(url_for('main.list_patients'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    return render_template('patients/add.html', form=form)
# GET请求：显示空表单
# POST请求：处理表单提交
# 数据验证：使用FlaskForm验证
# 事务处理：异常时自动回滚
# 用户反馈：成功或失败的消息提示

@main.route('/patients/edit/<patient_id>', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        try:
            db.session.commit()
            flash('患者信息更新成功')
            return redirect(url_for('main.list_patients'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    return render_template('patients/edit.html', form=form, patient=patient)
# 数据预填充：PatientForm(obj=patient)
# 自动更新：form.populate_obj(patient)
# 404处理：get_or_404() 自动处理不存在的记录

@main.route('/patients/view/<patient_id>')
#@login_required  # 移除这一行
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patients/view.html', patient=patient)


# ===== 部门管理 =====
@main.route('/departments')
#@login_required  # 移除这一行
def list_departments():
    departments = Department.query.all()
    return render_template('departments/list.html', departments=departments)
@main.route('/departments/view/<dept_id>')
def view_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    return render_template('departments/view.html', department=department)

@main.route('/departments/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(
            dept_id=form.dept_id.data,
            dept_name=form.dept_name.data,
            location=form.location.data,
            phone=form.phone.data,
            manager_id=form.manager_id.data
        )
        db.session.add(department)
        try:
            db.session.commit()
            flash('部门添加成功')
            return redirect(url_for('main.list_departments'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    return render_template('departments/add.html', form=form)


@main.route('/departments/edit/<dept_id>', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def edit_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        form.populate_obj(department)
        try:
            db.session.commit()
            flash('部门信息更新成功')
            return redirect(url_for('main.list_departments'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    return render_template('departments/edit.html', form=form, department=department)


# ===== 员工管理 =====
@main.route('/employees')
#@login_required  # 移除这一行
def list_employees():
    employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)
def view_employee(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    return render_template('employees/view.html', employee=employee)


@main.route('/employees/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            emp_id=form.emp_id.data,
            name=form.name.data,
            gender=form.gender.data,
            birth_date=form.birth_date.data,
            contact=form.contact.data,
            title=form.title.data,
            hire_date=form.hire_date.data,
            dept_id=form.dept_id.data
        )
        db.session.add(employee)
        try:
            db.session.commit()
            flash('员工添加成功')
            return redirect(url_for('main.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    return render_template('employees/add.html', form=form)


@main.route('/employees/edit/<emp_id>', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def edit_employee(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        form.populate_obj(employee)
        try:
            db.session.commit()
            flash('员工信息更新成功')
            return redirect(url_for('main.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')
    return render_template('employees/edit.html', form=form, employee=employee)

@main.route('/employees/view/<emp_id>')
#@login_required  # 移除这一行
def view_employee(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    return render_template('employees/view.html', employee=employee)


@main.route('/doctors/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            emp_id=form.emp_id.data,
            specialty=form.specialty.data,
            license_number=form.license_number.data
        )
        db.session.add(doctor)
        try:
            db.session.commit()
            flash('医生信息添加成功')
            return redirect(url_for('main.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    return render_template('employees/add_doctor.html', form=form)


# ===== 药品管理 =====
@main.route('/medicines')
#@login_required  # 移除这一行
def list_medicines():
    medicines = Medicine.query.all()
    return render_template('medicines/list.html', medicines=medicines)

@main.route('/medicines/view/<medicine_id>')
#@login_required  # 移除这一行
def view_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    return render_template('medicines/view.html', medicine=medicine)


@main.route('/medicines/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_medicine():
    form = MedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(
            medicine_id=form.medicine_id.data,
            name=form.name.data,
            specification=form.specification.data,
            manufacturer=form.manufacturer.data,
            price=form.price.data,
            stock_quantity=form.stock_quantity.data
        )
        db.session.add(medicine)
        try:
            db.session.commit()
            flash('药品添加成功')
            return redirect(url_for('main.list_medicines'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')
    return render_template('medicines/add.html', form=form)


@main.route('/medicines/edit/<medicine_id>', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def edit_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    form = MedicineForm(obj=medicine)

    if form.validate_on_submit():
        # 存储过程控制下的更新操作
        old_price = medicine.price
        new_price = form.price.data

        try:
            # 更新除价格外的其他属性
            medicine.name = form.name.data
            medicine.specification = form.specification.data
            medicine.manufacturer = form.manufacturer.data
            medicine.stock_quantity = form.stock_quantity.data

            # 调用存储过程更新价格
            result = db.session.execute(
                text('CALL update_medicine_price(:medicine_id, :new_price)'),
                {'medicine_id': medicine_id, 'new_price': new_price}
            )
            db.session.commit()
            flash(f'药品更新成功，价格已从 {old_price} 更新为 {new_price}')
            return redirect(url_for('main.list_medicines'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败: {str(e)}')

    return render_template('medicines/edit.html', form=form, medicine=medicine)


@main.route('/medicines/price_history/<medicine_id>')
#@login_required  # 移除这一行
def medicine_price_history(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    price_logs = PriceChangeLog.query.filter_by(medicine_id=medicine_id).order_by(
        PriceChangeLog.change_date.desc()).all()

    return render_template('medicines/price_history.html', medicine=medicine, logs=price_logs)


# ===== 处方管理 =====
@main.route('/prescriptions')
#@login_required  # 移除这一行
def list_prescriptions():
    # 含有视图的查询操作
    try:
        prescriptions = db.session.execute(text('SELECT * FROM doctor_prescription_view')).fetchall()
        return render_template('prescriptions/list.html', prescriptions=prescriptions)
    except Exception as e:
        flash(f'查询失败: {str(e)}')
        return render_template('prescriptions/list.html', prescriptions=[])


@main.route('/prescriptions/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_prescription():
    form = PrescriptionForm()

    # 获取可选医生列表
    doctors = db.session.query(Doctor.emp_id, Employee.name) \
        .join(Employee, Doctor.emp_id == Employee.emp_id).all()
    form.doctor_id.choices = [(d.emp_id, f"{d.emp_id} - {d.name}") for d in doctors]

    if form.validate_on_submit():
        prescription = Prescription(
            prescription_id=form.prescription_id.data,
            doctor_id=form.doctor_id.data,
            issue_time=datetime.now(),
            total_amount=form.total_amount.data
        )
        db.session.add(prescription)
        try:
            db.session.commit()
            flash('处方添加成功')
            return redirect(url_for('main.prescription_detail', prescription_id=prescription.prescription_id))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')

    # 生成唯一的处方ID
    if not form.prescription_id.data:
        form.prescription_id.data = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return render_template('prescriptions/add.html', form=form)


@main.route('/prescriptions/detail/<prescription_id>', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def prescription_detail(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    form = PrescriptionDetailForm()

    # 获取可选药品列表
    medicines = Medicine.query.all()
    form.medicine_id.choices = [(m.medicine_id, f"{m.medicine_id} - {m.name} ({m.specification})") for m in medicines]

    if form.validate_on_submit():
        # 触发器控制下的添加操作
        detail = PrescriptionDetail(
            prescription_id=prescription_id,
            medicine_id=form.medicine_id.data,
            quantity=form.quantity.data,
            usage=form.usage.data
        )
        db.session.add(detail)
        try:
            db.session.commit()

            # 重新计算总金额（正确方式）
            total_amount = db.session.query(
                func.sum(PrescriptionDetail.quantity * Medicine.price)
            ).join(Medicine).filter(
                PrescriptionDetail.prescription_id == prescription_id
            ).scalar() or 0

            prescription.total_amount = total_amount
            db.session.commit()
            flash('药品添加成功')
            return redirect(url_for('main.prescription_detail', prescription_id=prescription_id))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')

    details = []
    for detail in prescription.details:
        medicine = Medicine.query.get(detail.medicine_id)
        if medicine:
            details.append({
                'id': detail.id,
                'name': medicine.name,
                'specification': medicine.specification,
                'quantity': detail.quantity,
                'usage': detail.usage,
                'price': medicine.price,
                'total_price': medicine.price * detail.quantity
            })

    return render_template('prescriptions/detail.html',
                           prescription=prescription,
                           form=form,
                           details=details)


# 含有事务应用的删除操作
@main.route('/prescriptions/delete/<prescription_id>', methods=['POST'])
#@login_required  # 移除这一行
def delete_prescription(prescription_id):
    try:
        # 开始事务
        db.session.begin_nested()

        # 先删除处方明细
        PrescriptionDetail.query.filter_by(prescription_id=prescription_id).delete()

        # 更新相关医疗记录
        MedicalRecord.query.filter_by(prescription_id=prescription_id).update({MedicalRecord.prescription_id: None})

        # 删除处方
        Prescription.query.filter_by(prescription_id=prescription_id).delete()

        # 提交事务
        db.session.commit()
        flash('处方删除成功')
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        flash(f'删除失败: {str(e)}')

    return redirect(url_for('main.list_prescriptions'))


# 删除处方明细
@main.route('/prescription_detail/delete/<int:detail_id>', methods=['POST'])
#@login_required  # 移除这一行
def delete_prescription_detail(detail_id):
    detail = PrescriptionDetail.query.get_or_404(detail_id)
    prescription_id = detail.prescription_id

    try:
        # 获取该明细的金额，用于更新处方总金额
        medicine = Medicine.query.get(detail.medicine_id)
        detail_amount = medicine.price * detail.quantity

        # 更新处方总金额
        prescription = Prescription.query.get(prescription_id)
        prescription.total_amount -= detail_amount

        # 删除明细
        db.session.delete(detail)
        db.session.commit()
        flash('药品移除成功')
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        flash(f'移除失败: {str(e)}')

    return redirect(url_for('main.prescription_detail', prescription_id=prescription_id))


# ===== 医疗记录管理 =====
@main.route('/medical_records/add', methods=['GET', 'POST'])
#@login_required  # 移除这一行
def add_medical_record():
    form = MedicalRecordForm()

    # 获取可选患者列表
    patients = Patient.query.all()
    form.patient_id.choices = [(p.patient_id, f"{p.patient_id} - {p.name}") for p in patients]

    # 获取可选医生列表
    doctors = db.session.query(Doctor.emp_id, Employee.name) \
        .join(Employee, Doctor.emp_id == Employee.emp_id).all()
    form.doctor_id.choices = [(d.emp_id, f"{d.emp_id} - {d.name}") for d in doctors]

    # 获取可选处方列表
    prescriptions = Prescription.query.all()
    form.prescription_id.choices = [('', '-- 不关联处方 --')] + \
                                   [(p.prescription_id, f"{p.prescription_id} - {p.issue_time}") for p in prescriptions]

    if form.validate_on_submit():
        record = MedicalRecord(
            record_id=form.record_id.data,
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            visit_time=form.visit_time.data or datetime.now(),
            diagnosis=form.diagnosis.data,
            prescription_id=form.prescription_id.data or None
        )
        db.session.add(record)
        try:
            db.session.commit()
            flash('医疗记录添加成功')
            return redirect(url_for('main.view_patient', patient_id=form.patient_id.data))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败: {str(e)}')

    # 生成唯一的记录ID
    if not form.record_id.data:
        form.record_id.data = f"MR{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return render_template('medical_records/add.html', form=form)


# ===== 统计报表 =====
@main.route('/reports/department_prescriptions')
#@login_required  # 移除这一行
def report_department_prescriptions():
    # 统计各科室开具处方数量和总金额
    try:
        stats = db.session.execute(text("""
                                        SELECT d.dept_name, COUNT(p.prescription_id) as count, SUM(p.total_amount) as total
                                        FROM prescription p
                                            JOIN doctor doc
                                        ON p.doctor_id = doc.emp_id
                                            JOIN employee e ON doc.emp_id = e.emp_id
                                            JOIN department d ON e.dept_id = d.dept_id
                                        GROUP BY d.dept_name
                                        ORDER BY COUNT (p.prescription_id) DESC
                                        """)).fetchall()

        return render_template('reports/department_prescriptions.html', stats=stats)
    except Exception as e:
        flash(f'统计失败: {str(e)}')
        return render_template('reports/department_prescriptions.html', stats=[])


@main.route('/reports/medicine_usage')
#@login_required  # 移除这一行
def report_medicine_usage():
    # 统计药品使用情况
    try:
        stats = db.session.execute(text("""
                                        SELECT m.name,
                                               m.specification,
                                               SUM(pd.quantity)                  as total_used,
                                               COUNT(DISTINCT p.prescription_id) as prescriptions_count,
                                               m.stock_quantity                  as current_stock
                                        FROM medicine m
                                                 LEFT JOIN prescription_detail pd ON m.medicine_id = pd.medicine_id
                                                 LEFT JOIN prescription p ON pd.prescription_id = pd.prescription_id
                                        GROUP BY m.medicine_id, m.name, m.specification, m.stock_quantity
                                        ORDER BY SUM(pd.quantity) DESC
                                        """)).fetchall()

        return render_template('reports/medicine_usage.html', stats=stats)
    except Exception as e:
        flash(f'统计失败: {str(e)}')
        return render_template('reports/medicine_usage.html', stats=[])


# ===== API 接口 =====
@main.route('/api/medicines')
#@login_required  # 移除这一行
def api_medicines():
    medicines = Medicine.query.all()
    result = [{
        'id': m.medicine_id,
        'name': m.name,
        'specification': m.specification,
        'price': float(m.price),
        'stock': m.stock_quantity
    } for m in medicines]
    return jsonify(result)


@main.route('/api/chart/department_stats')
#@login_required  # 移除这一行
def api_chart_department_stats():
    try:
        stats = db.session.execute(text("""
                                        SELECT d.dept_name, COUNT(p.prescription_id) as prescription_count
                                        FROM department d
                                                 LEFT JOIN employee e ON d.dept_id = e.dept_id
                                                 LEFT JOIN doctor doc ON e.emp_id = doc.emp_id
                                                 LEFT JOIN prescription p ON doc.emp_id = p.doctor_id
                                        GROUP BY d.dept_name
                                        """)).fetchall()

        labels = [row.dept_name for row in stats]
        data = [row.prescription_count for row in stats]

        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': '处方数量',
                'data': data,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                'borderWidth': 1
            }]
        }

        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# 数据格式化：符合Chart.js要求的数据结构
# 颜色配置：预定义的图表颜色方案
# 错误处理：API级别的错误响应
