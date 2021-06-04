/*Write a SQL query to find the number of matches thatwere 
won by a single point, butdo not include matches decided by penalty shootout*/
with normal as (
select goal_score,left(goal_score,1) as left_side, right(goal_score, 1) as right_side,
position('-' in goal_score) as Position, length(goal_score) as length,
case when decided_by != 'P' then 'True' end as test
from euro_cup_2016.match_mast
where decided_by != 'P'
having length =3),

with abnormal as (
select goal_score,left(goal_score,1) as left_side, right(goal_score, 1) as right_side,
position('-' in goal_score) as Position, length(goal_score) as length,
case when decided_by != 'P' then 'True' end as test
from euro_cup_2016.match_mast
where decided_by != 'P'
having length =6)

select 
*
from CTE


