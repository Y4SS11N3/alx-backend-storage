-- SafeDiv: Safely divides two integers, returning 0 if the divisor is 0
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN b = 0 THEN 0
        ELSE a * 1.0 / b
    END;
END$$
DELIMITER ;
