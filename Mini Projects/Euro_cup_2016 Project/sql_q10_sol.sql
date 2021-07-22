/*Write a SQL query to find all available informationabout the 
players under contract toLiverpool F.C. playing for England in EURO Cup 2016.*/
SELECT *
FROM euro_cup_2016.player_mast mast
INNER JOIN euro_cup_2016.soccer_country country
ON mast.team_id = country.country_id
WHERE playing_club = 'Liverpool'
AND country_name = 'England';









