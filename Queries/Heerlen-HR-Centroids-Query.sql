copy (select uuid, ST_AsText(ti.area) as Area, ST_AsText(ST_Centroid(ti.area)) as Point from areaofinterest as ai
inner join tiles as ti on ti.area_id = ai.area_id and ai.area_id = 15
inner join tile_files as tf on ti.tile_id = tf.tile_id and tf.year = 2018 and tf.layername = 'rgb_hr_2018'
) to '/tmp/Heerlen-HR-centroids.csv' with (format csv, header); 
