/*Write a SQL query to find the number of captains whowere also goalkeepers.*/

select  count(*) as number_captain
from euro_cup_2016.match_captain captain
left join euro_cup_2016.player_mast mast
on captain.team_id=mast.team_id
where posi_to_play = 'GK'

order by number_captain desc


















