/*Write a SQL query to find the substitute players whocame 
into the field in the firsthalf of play, within a normal play schedule.*/

select distinct player_name as player
from euro_cup_2016.player_mast mast
left join euro_cup_2016.player_in_out ex
on mast.player_id=ex.player_id
where in_out='I' and play_schedule='NT' and play_half=2


















