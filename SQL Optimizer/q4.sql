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

-- 4. List the names of students who have taken a course taught by professor v5 (name).
/* Optimization: Modify the query to use a CTE to remove the inner hash join. Overall run time decreased to 0.750 ms from 11.149 ms.
				Removed alias 2 from the original query as it was unused in the execution plan.
*/

explain analyze with cte as (
select studId
from Transcript
where crsCode in (select crsCode from Professor
                  left join Teaching 
                  on Professor.id=Teaching.profId
                  where Professor.name = @v5))
select name from Student
join cte on cte.studId=Student.id