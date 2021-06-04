/*Write a SQL query to find all the defenders who scoreda goal for their teams.*/


select player_name as player
from euro_cup_2016.player_mast mast
left join euro_cup_2016.goal_details goals
on mast.player_id=goals.player_id
where mast.posi_to_play='FD' and goals.goal_id !=0
order by player asc












