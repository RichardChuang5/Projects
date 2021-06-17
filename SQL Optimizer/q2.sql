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

-- 2. List the names of students with id in the range of v2 (id) to v3 (inclusive).
-- Optimization:
	-- Change between to in. This allows the index to be used and creates an overall actual time of 
    -- 0.031 as opposed to 0.042 in the original query.

explain analyze SELECT name FROM Student WHERE id in (@v2,@v3);