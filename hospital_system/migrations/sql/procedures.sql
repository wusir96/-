-- 确保使用正确的数据库
USE hospital_system;

-- 设置分隔符
DELIMITER //

-- 删除已存在的存储过程（如果存在）
DROP PROCEDURE IF EXISTS update_medicine_price //
DROP PROCEDURE IF EXISTS admit_patient //
DROP PROCEDURE IF EXISTS discharge_patient //

-- 更新药品价格（含价格变动规则）
CREATE PROCEDURE update_medicine_price(
    IN med_id VARCHAR(20),
    IN new_price DECIMAL(10,2)
)
BEGIN
    DECLARE old_price DECIMAL(10,2);

    -- 获取旧价格
    SELECT price INTO old_price
    FROM medicine
    WHERE medicine_id = med_id;

    -- 价格验证规则
    IF new_price < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '药品价格不能为负数';
    ELSEIF new_price > old_price * 1.5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '药品价格涨幅过大，不得超过原价的50%';
    ELSE
        -- 更新价格
        UPDATE medicine
        SET price = new_price
        WHERE medicine_id = med_id;

        -- 记录价格变更历史
        INSERT INTO price_change_log(medicine_id, old_price, new_price, change_date)
        VALUES (med_id, old_price, new_price, NOW());
    END IF;
END //

-- 处理患者入院
CREATE PROCEDURE admit_patient(
    IN p_patient_id VARCHAR(20),
    IN p_ward_id VARCHAR(10),
    IN p_doctor_id VARCHAR(20),
    IN p_diagnosis VARCHAR(200)
)
BEGIN
    DECLARE v_record_id VARCHAR(20);
    DECLARE v_available_beds INT;

    -- 检查病房是否有空床位
    SELECT available_beds INTO v_available_beds
    FROM ward
    WHERE ward_id = p_ward_id;

    IF v_available_beds <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '所选病房没有可用床位';
    ELSE
        -- 生成住院记录ID
        SET v_record_id = CONCAT('MR', DATE_FORMAT(NOW(), '%Y%m%d'), FLOOR(RAND() * 1000));

        -- 创建医疗记录
        INSERT INTO medical_record(record_id, patient_id, doctor_id, visit_time, diagnosis, ward_id)
        VALUES (v_record_id, p_patient_id, p_doctor_id, NOW(), p_diagnosis, p_ward_id);

        -- 更新病房可用床位数
        UPDATE ward
        SET available_beds = available_beds - 1
        WHERE ward_id = p_ward_id;

        -- 返回创建的记录ID
        SELECT v_record_id AS admission_record_id;
    END IF;
END //

-- 处理患者出院
CREATE PROCEDURE discharge_patient(
    IN p_record_id VARCHAR(20)
)
BEGIN
    DECLARE v_ward_id VARCHAR(10);

    -- 获取患者的病房ID
    SELECT ward_id INTO v_ward_id
    FROM medical_record
    WHERE record_id = p_record_id;

    -- 如果存在病房记录，则更新可用床位
    IF v_ward_id IS NOT NULL THEN
        -- 更新病房可用床位数
        UPDATE ward
        SET available_beds = available_beds + 1
        WHERE ward_id = v_ward_id;
    END IF;

    -- 更新医疗记录，标记患者已出院
    UPDATE medical_record
    SET discharge_time = NOW()
    WHERE record_id = p_record_id;

    SELECT 'Patient discharged successfully' AS result;
END //

-- 恢复默认分隔符
DELIMITER ;