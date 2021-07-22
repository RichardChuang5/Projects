/*Write a SQL query to find all the venues where matcheswith penalty shootouts wereplayed.*/


select distinct venue.venue_name as Location
from euro_cup_2016.soccer_venue as venue
left join euro_cup_2016.match_mast as mast
on venue.venue_id=mast.venue_id
left join euro_cup_2016.penalty_shootout as shoot
on mast.match_no=shoot.match_no
where kick_id !=0






