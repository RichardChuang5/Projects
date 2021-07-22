/*Write a SQL query to find the match number, date,
and score for matches in which nostoppage time was added in the 1st half.*/
select master.match_no, master.play_date,details.team_id, details.goal_score
from euro_cup_2016.match_mast as master
left join euro_cup_2016.match_details as details
on master.match_no=details.match_no
where stop1_sec =0