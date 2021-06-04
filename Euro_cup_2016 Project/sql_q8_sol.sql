/*Write a SQL query to find the match number for thegame 
with the highest number ofpenalty shots, and which countries played that match*/


select shoot.match_no, sum(kick_no) as Highest_Kicks, country.country_id, country.country_name
from euro_cup_2016.penalty_shootout as shoot
left join euro_cup_2016.match_mast as mast
on shoot.match_no=mast.match_no
left join euro_cup_2016.soccer_venue as venue
on mast.venue_id=venue.venue_id
left join euro_cup_2016.soccer_city as city
on venue.city_id=city.city_id
left join euro_cup_2016.soccer_country as country
on city.country_id=country.country_id
group by shoot.match_no
order by Highest_Kicks desc
limit 1








