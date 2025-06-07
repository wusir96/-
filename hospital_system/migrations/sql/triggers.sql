-- filepath: d:\桌面\hospital_system\migrations\sql\triggers.sql
-- 确保使用正确的数据库
USE hospital_system;

-- 设置分隔符，方便创建触发器
DELIMITER //

-- 删除已存在的触发器（如果存在）
DROP TRIGGER IF EXISTS check_medicine_stock //
DROP TRIGGER IF EXISTS update_medicine_stock //
DROP TRIGGER IF EXISTS reduce_medicine_stock //
DROP TRIGGER IF EXISTS restore_medicine_stock //
DROP TRIGGER IF EXISTS adjust_medicine_stock //
-- DROP TRIGGER IF EXISTS check_ward_beds //  -- 删除此行

-- 在添加处方明细前检查药品库存是否足够
CREATE TRIGGER check_medicine_stock
BEFORE INSERT ON prescription_detail
FOR EACH ROW
BEGIN
    DECLARE current_stock INT;

    -- 获取当前库存
    SELECT stock_quantity INTO current_stock
    FROM medicine
    WHERE medicine_id = NEW.medicine_id;

    -- 检查库存是否足够
    IF current_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '药品库存不足，无法开具处方';
    END IF;
END //

-- 恢复默认分隔符
DELIMITER ;

-- 设置分隔符，方便创建触发器
DELIMITER //

-- 更新处方明细时也检查库存
CREATE TRIGGER update_medicine_stock
BEFORE UPDATE ON prescription_detail
FOR EACH ROW
BEGIN
    DECLARE current_stock INT;
    DECLARE stock_diff INT;

    -- 计算库存差额
    SET stock_diff = NEW.quantity - OLD.quantity;

    -- 只有在数量增加时才检查
    IF stock_diff > 0 THEN
        -- 获取当前库存
        SELECT stock_quantity INTO current_stock
        FROM medicine
        WHERE medicine_id = NEW.medicine_id;

        -- 检查库存是否足够
        IF current_stock < stock_diff THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '药品库存不足，无法更新处方';
        END IF;
    END IF;
END //

-- 恢复默认分隔符
DELIMITER ;

-- 设置分隔符，方便创建触发器
DELIMITER //

-- 添加处方明细后减少药品库存
CREATE TRIGGER reduce_medicine_stock
AFTER INSERT ON prescription_detail
FOR EACH ROW
BEGIN
    -- 减少对应药品的库存
    UPDATE medicine
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE medicine_id = NEW.medicine_id;
END //

-- 恢复默认分隔符
DELIMITER ;

-- 设置分隔符，方便创建触发器
DELIMITER //

-- 删除处方明细后恢复药品库存
CREATE TRIGGER restore_medicine_stock
AFTER DELETE ON prescription_detail
FOR EACH ROW
BEGIN
    -- 恢复对应药品的库存
    UPDATE medicine
    SET stock_quantity = stock_quantity + OLD.quantity
    WHERE medicine_id = OLD.medicine_id;
END //

-- 恢复默认分隔符
DELIMITER ;

-- 设置分隔符，方便创建触发器
DELIMITER //

-- 更新处方明细后调整药品库存
CREATE TRIGGER adjust_medicine_stock
AFTER UPDATE ON prescription_detail
FOR EACH ROW
BEGIN
    -- 调整药品库存（可能增加或减少）
    UPDATE medicine
    SET stock_quantity = stock_quantity + (OLD.quantity - NEW.quantity)
    WHERE medicine_id = NEW.medicine_id;
END //

-- 恢复默认分隔符
DELIMITER ;

-- 设置分隔符，方便创建触发器
-- DELIMITER //  -- 删除此行

-- 病房床位检查触发器
-- CREATE TRIGGER check_ward_beds  -- 删除此行
-- BEFORE INSERT ON medical_record  -- 删除此行
-- FOR EACH ROW  -- 删除此行
-- BEGIN  -- 删除此行
--     -- 声明变量必须在 BEGIN 块的开头  -- 删除此行
--     DECLARE available INT;  -- 删除此行

--     -- 如果包含病房信息，则检查床位是否可用  -- 删除此行
--     IF NEW.ward_id IS NOT NULL THEN  -- 删除此行
--         -- 获取可用床位数  -- 删除此行
--         SELECT available_beds INTO available  -- 删除此行
--         FROM ward  -- 删除此行
--         WHERE ward_id = NEW.ward_id;  -- 删除此行

--         -- 检查是否有可用床位  -- 删除此行
--         IF available <= 0 THEN  -- 删除此行
--             SIGNAL SQLSTATE '45000'  -- 删除此行
--             SET MESSAGE_TEXT = '所选病房没有可用床位';  -- 删除此行
--         END IF;  -- 删除此行
--     END IF;  -- 删除此行
-- END //  -- 删除此行

-- 恢复默认分隔符
-- DELIMITER ;  -- 删除此行