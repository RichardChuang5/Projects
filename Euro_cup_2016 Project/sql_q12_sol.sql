/*Write a SQL query that returns the total number ofgoals scored 
by each position oneach country’s team. Do not include positions whichscored no goals*/
select  posi_to_play as position, country_name as country, COUNT(goal_id) as goals_scored
from euro_cup_2016.player_mast mast
left join euro_cup_2016.goal_details goals
on mast.player_id = goals.player_id
left join euro_cup_2016.soccer_country country
on mast.team_id = country.country_id
group by 1,2
order by goals_scored desc









