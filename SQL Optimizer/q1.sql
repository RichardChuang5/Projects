USE springboardopt;

-- -------------------------------------
SET @v1 = 1612521;
SET @v2 = 1145072;
SET @v3 = 1828467;
SET @v4 = 'MGT382';
SET @v5 = 'Amber Hill';
SET @v6 = 'MGT';
SET @v7 = 'EE';			  
SET @v8 = 'MAT';

-- 1. List the name of the student with id equal to v1 (id).
	-- Observations:
		-- original time to run is 0.09 ms
	-- Changes and effect:
		-- Include an index. Reduces the actual time down to 0.024

explain analyze SELECT name FROM Student WHERE id = @v1;