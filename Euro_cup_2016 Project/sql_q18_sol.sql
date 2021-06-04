/*Write a SQL query to find the highest number of foulcards given in one match.*/

select match_no, count(*) as foul_cards
from euro_cup_2016.player_booked
group by 1
order by foul_cards desc


















