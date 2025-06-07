-- filepath: d:\桌面\hospital_system\migrations\sql\views.sql
-- 确保使用正确的数据库
USE hospital_system;

-- 删除已存在的视图（如果存在）
DROP VIEW IF EXISTS doctor_prescription_view;
DROP VIEW IF EXISTS medicine_stock_alert;
DROP VIEW IF EXISTS patient_medical_history;
DROP VIEW IF EXISTS doctor_workload;

-- 医生处方视图：关联医生、科室和处方信息
CREATE VIEW doctor_prescription_view AS
SELECT
    p.prescription_id,
    p.issue_time,
    p.total_amount,
    d.emp_id AS doctor_id,
    e.name AS doctor_name,
    dept.dept_name,
    dept.dept_id
FROM prescription p
JOIN doctor d ON p.doctor_id = d.emp_id
JOIN employee e ON d.emp_id = e.emp_id
JOIN department dept ON e.dept_id = dept.dept_id;
--业务目标：关联医生、科室和处方信息，提供完整的处方概览
-- 表连接：prescription → doctor → employee → department
-- 应用场景：
-- 处方管理页面显示
-- 医生工作量统计
-- 科室处方分析
-- 药品库存预警视图：显示库存低于阈值的药品
CREATE VIEW medicine_stock_alert AS
SELECT
    medicine_id,
    name,
    specification,
    manufacturer,
    price,
    stock_quantity,
    CASE
        WHEN stock_quantity = 0 THEN '无库存'
        WHEN stock_quantity < 10 THEN '库存紧张'
        WHEN stock_quantity < 30 THEN '库存较低'
        ELSE '库存充足'
    END AS stock_status
FROM medicine
WHERE stock_quantity < 30
ORDER BY stock_quantity;
-- 业务目标：药品库存监控和预警
-- 智能分级：
-- 0 个：无库存（红色警告）
-- 1-9 个：库存紧张（橙色警告）
-- 10-29 个：库存较低（黄色提醒）
-- 筛选条件：只显示库存少于30的药品
-- 排序规则：按库存数量升序排列

-- 患者医疗记录视图：整合患者、医生和处方信息
CREATE VIEW patient_medical_history AS
SELECT
    mr.record_id,
    mr.visit_time,
    -- mr.discharge_time,  -- 移除此行
    p.patient_id,
    p.name AS patient_name,
    p.gender,
    e.name AS doctor_name,
    dept.dept_name,
    mr.diagnosis,
    IFNULL(pres.prescription_id, '无处方') AS prescription_id,
    IFNULL(pres.total_amount, 0) AS prescription_amount
FROM medical_record mr
JOIN patient p ON mr.patient_id = p.patient_id
JOIN doctor d ON mr.doctor_id = d.emp_id
JOIN employee e ON d.emp_id = e.emp_id
JOIN department dept ON e.dept_id = dept.dept_id
LEFT JOIN prescription pres ON mr.prescription_id = pres.prescription_id
ORDER BY p.patient_id, mr.visit_time DESC;
-- 业务目标：整合患者完整的医疗历史信息
-- 连接方式：
-- JOIN：确保有医生和科室信息的记录
-- LEFT JOIN：包含没有处方的医疗记录
-- 数据处理：
-- IFNULL(pres.prescription_id, '无处方')：处理空值显示
-- IFNULL(pres.total_amount, 0)：确保金额不为空
-- 排序规则：按患者ID分组，每组内按就诊时间倒序
-- 科室医生工作量统计视图
CREATE VIEW doctor_workload AS
SELECT
    e.emp_id,
    e.name AS doctor_name,
    dept.dept_name,
    COUNT(DISTINCT mr.record_id) AS patient_count,
    COUNT(DISTINCT p.prescription_id) AS prescription_count,
    SUM(IFNULL(p.total_amount, 0)) AS total_prescription_amount
FROM employee e
JOIN doctor d ON e.emp_id = d.emp_id
JOIN department dept ON e.dept_id = dept.dept_id
LEFT JOIN medical_record mr ON d.emp_id = mr.doctor_id
LEFT JOIN prescription p ON d.emp_id = p.doctor_id
GROUP BY e.emp_id, e.name, dept.dept_name
ORDER BY patient_count DESC;