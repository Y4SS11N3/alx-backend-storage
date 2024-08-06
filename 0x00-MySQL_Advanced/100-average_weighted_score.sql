-- Create stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_weighted_score FLOAT;

    -- Compute average weighted score
    SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
    INTO avg_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Update user's average_score
    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id;
END //
DELIMITER ;
