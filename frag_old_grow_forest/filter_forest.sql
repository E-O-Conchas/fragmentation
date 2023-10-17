
-- create a fragmentation patches

CREATE TABLE fragmentation.frag_patches AS
SELECT * FROM (
	SELECT * FROM fragmentation.land_cover_primary_forest_points
	UNION ALL
	SELECT * FROM fragmentation.land_cover_primary_forest_polygons
) AS land_cover_x_primary_forest
WHERE code_18 IN ('311', '312', '313', '321', '322', '324');


-- 311 -> Broad leaved forest
-- 312 -> Coniferous forest
-- 313 -> Mixed forest
-- 321 -> Natural grasslands
-- 322 -> Moors and heathland
-- 324 -> Transitional woodland-shrub
 
SELECT * FROM fragmentation.frag_patches



-- create a fragmentation patches for Estonia

CREATE TABLE fragmentation.frag_patches_estonia AS
SELECT * FROM fragmentation."land_cover_primary_forest_polygons_EE"









