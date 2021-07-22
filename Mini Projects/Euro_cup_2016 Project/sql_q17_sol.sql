/*Write a SQL query to find the country where the 
mostassistant referees come from,and the count of the assistant referees*/

select country_name, count(*) as num_country
from euro_cup_2016.asst_referee_mast mast
left join euro_cup_2016.soccer_country country
on mast.country_id=country.country_id
group by 1
order by num_country desc


















