-- Drop existing SafeDiv function if it exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Create function SafeDiv with high precision
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DOUBLE PRECISION DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a * 1.0 / b;
    END IF;
END //
DELIMITER ;
