Forecast this professional League of Legends game at the observation point in
./snapshot.json. You may inspect that file with local tools. History contains archived
game outcomes and player box scores. In a Fearless series, earlier picks by either team
are unavailable to both teams. There is no live search. Write ./prediction.json with
exactly two numeric probabilities from 0 to 1: p_blue_win (blue wins this game) and
p_blue_ahead_15 (blue's gold exceeds red's at 15:00; a tie counts as false).
Reward is one minus the equally weighted mean of the two squared probability errors.
