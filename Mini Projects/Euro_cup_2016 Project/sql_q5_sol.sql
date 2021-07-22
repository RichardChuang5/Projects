/*Write a SQL query to find the number of bookings thathappened in stoppage time*/
select count(*) as Stoppage_Goals
from euro_cup_2016.player_booked as players 
where play_schedule ='ST'
