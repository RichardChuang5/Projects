/*Write a SQL query to compute a list showing the numberof substitutions thathappened in 
various stages of play for the entiretournament..*/
select team_id, count(in_out) as Substitutions
from euro_cup_2016.player_in_out
group by 1