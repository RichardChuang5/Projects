/*Write a SQL query to find the number of matches that were won by penalty shootout.*/
select count(*) as Penalty_Win
from euro_cup_2016.match_mast
where decided_by = 'P'