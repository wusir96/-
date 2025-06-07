-- 注意：此文件可能不需要，因为表结构通过SQLAlchemy ORM创建
-- 如果需要直接创建表，可以使用以下SQL

-- 创建患者表
CREATE TABLE IF NOT EXISTS patient (
    patient_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(1),
    birth_date DATE,
    contact VARCHAR(20),
    address VARCHAR(100),
    insurance_number VARCHAR(30)
);

-- 创建科室表
CREATE TABLE IF NOT EXISTS department (
    dept_id VARCHAR(10) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    location VARCHAR(50),
    phone VARCHAR(15),
    manager_id VARCHAR(20)
);

-- 创建员工表
CREATE TABLE IF NOT EXISTS employee (
    emp_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(1),
    birth_date DATE,
    contact VARCHAR(20),
    title VARCHAR(30),
    hire_date DATE,
    dept_id VARCHAR(10),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

-- 添加科室表的外键约束
ALTER TABLE department
ADD CONSTRAINT fk_manager
FOREIGN KEY (manager_id) REFERENCES employee(emp_id);

-- 创建医生表
CREATE TABLE IF NOT EXISTS doctor (
    emp_id VARCHAR(20) PRIMARY KEY,
    specialty VARCHAR(50),
    license_number VARCHAR(30) UNIQUE,
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

-- 创建护士表
CREATE TABLE IF NOT EXISTS nurse (
    emp_id VARCHAR(20) PRIMARY KEY,
    nursing_level VARCHAR(20),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

-- 创建药品表
CREATE TABLE IF NOT EXISTS medicine (
    medicine_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    specification VARCHAR(50),
    manufacturer VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT
);

-- 创建病房表
CREATE TABLE IF NOT EXISTS ward (
    ward_id VARCHAR(10) PRIMARY KEY,
    ward_type VARCHAR(20),
    bed_count INT,
    available_beds INT,
    dept_id VARCHAR(10),
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
);

-- 创建处方表
CREATE TABLE IF NOT EXISTS prescription (
    prescription_id VARCHAR(20) PRIMARY KEY,
    doctor_id VARCHAR(20),
    issue_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (doctor_id) REFERENCES doctor(emp_id)
);

-- 创建医疗记录表
CREATE TABLE IF NOT EXISTS medical_record (
    record_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(20),
    visit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    diagnosis VARCHAR(200),
    prescription_id VARCHAR(20),
    ward_id VARCHAR(10),
    discharge_time DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(emp_id),
    FOREIGN KEY (prescription_id) REFERENCES prescription(prescription_id),
    FOREIGN KEY (ward_id) REFERENCES ward(ward_id)
);

-- 创建处方明细表
CREATE TABLE IF NOT EXISTS prescription_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prescription_id VARCHAR(20),
    medicine_id VARCHAR(20),
    quantity INT,
    usage VARCHAR(100),
    FOREIGN KEY (prescription_id) REFERENCES prescription(prescription_id),
    FOREIGN KEY (medicine_id) REFERENCES medicine(medicine_id)
);

-- 创建价格变更日志表
CREATE TABLE IF NOT EXISTS price_change_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id VARCHAR(20),
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicine_id) REFERENCES medicine(medicine_id)
);