-- List Glam rock bands by their longevity
SELECT band_name, 
       IFNULL(GREATEST(IFNULL(split, 2022) - formed, 0), 0) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
