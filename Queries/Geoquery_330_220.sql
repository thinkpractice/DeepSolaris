copy
(
	select ti.uuid as UUID_330, ST_AsText(ST_Centroid(ti.area)) as Centroid_330, h.uuid as UUID_220, ST_AsText(ST_Centroid(h.area)) as Centroid_220  from Tiles as ti
	inner join
	(
	select tt.uuid, tt.area from Tiles as tt
	where tt.area_id = 19
	) h
	on ST_Within(h.area, ti.area)
	where ti.area_id = 28
)
to '/tmp/hr_330_to_220.csv' delimiter ';' csv header;
