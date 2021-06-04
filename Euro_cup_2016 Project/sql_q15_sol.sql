/*Write a SQL query to find the referees who bookedthe most number of players.*/

select referee_name as referee, count(*) as bookings
from euro_cup_2016.referee_mast mast
left join euro_cup_2016.soccer_country country
on mast.country_id=country.country_id
left join euro_cup_2016.player_booked booked
on country.country_id=booked.team_id
group by 1
order by bookings desc












