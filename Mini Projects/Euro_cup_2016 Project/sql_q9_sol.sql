/*Write a SQL query to find the goalkeeper’s name andjersey number, 
playing forGermany, who played in Germany’s group stage matches.*/

/*NOTE: the city table only houses French cities and thus all the country names are going to appear as France.
*/


select player.player_name, player.jersey_no, country.country_name
from euro_cup_2016.player_mast as player
left join euro_cup_2016.soccer_team as team
on player.team_id=team.team_id
left join euro_cup_2016.match_details as details
on team.team_id =details.team_id
left join euro_cup_2016.match_mast as mast
on details.match_no=mast.match_no
left join euro_cup_2016.soccer_venue as venue
on mast.venue_id=venue.venue_id
left join euro_cup_2016.soccer_city as city
on venue.city_id=city.city_id
left join euro_cup_2016.soccer_country as country
on city.country_id = country.country_id
where player.posi_to_play='GK' and details.play_stage = 'G'
group by 1,2

/*and country.country_name='Germany'
player.player_name, player.jersey_no, details.play_stage, country.country_name as country
*/









