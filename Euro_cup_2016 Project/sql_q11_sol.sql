/*Write a SQL query to find the players, their jerseynumber, 
and playing club who werethe goalkeepers for England in EURO Cup 2016.*/
SELECT player_name as player, jersey_no as jersey, playing_club as club
FROM euro_cup_2016.player_mast mast
INNER JOIN euro_cup_2016.soccer_country country
ON mast.team_id = country.country_id
WHERE posi_to_play = 'GK'
AND country_name = 'England'









