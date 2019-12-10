select count(*) from register_label_per_building
select count(*) from annotations_per_tile_geo

select 	ag.uuid, 
	ST_Intersection(ag.tile_geom, rb.geovlak) as intersection_geom,
	ST_Area(ST_Intersection(ag.tile_geom, rb.geovlak)) as intersection_area
from annotations_per_tile_geo as ag
inner join register_label_per_building as rb on ST_Intersects(ag.tile_geom, rb.geovlak)
where ST_Area(ST_Intersection(ag.tile_geom, rb.geovlak)) > 1
order by ST_Area(ST_Intersection(ag.tile_geom, rb.geovlak)) asc

select ag.uuid, count(*) from annotations_per_tile_geo as ag
inner join register_label_per_building as rb on ST_Intersects(ag.tile_geom, rb.geovlak)
group by ag.uuid
having max(rb.register_label) <> max(ag.label)

drop table register_vs_annotations;
create table register_vs_annotations
as
select 
	ag.*, 
	a.register_label, 
	a.num_buildings,
	a.min_intersection_area,
	a.max_intersection_area,
	a.year_in_use,
	a.date_in_use
from annotations_per_tile_geo as ag
inner join (
	select 
		ag.uuid, 
		max(rb.register_label) as register_label, 
		count(*) as num_buildings, 
		max(year_in_use) as year_in_use,
		max(date_in_use) as date_in_use,
		min(ST_Area(ST_Intersection(ag.tile_geom, rb.geovlak))) as min_intersection_area,
		max(ST_Area(ST_Intersection(ag.tile_geom, rb.geovlak))) as max_intersection_area
	from annotations_per_tile_geo as ag
	inner join register_label_per_building as rb on ST_Intersects(ag.tile_geom, rb.geovlak)
	group by ag.uuid
	--having max(rb.register_label) <> max(ag.label)
) a on ag.uuid = a.uuid
order by ag.uuid


alter table register_vs_annotations
add constraint pk_register_vs_annotations primary key (id);

CREATE INDEX "register_vs_annotations_tile_geom_index" ON "register_vs_annotations" USING gist (tile_geom);

drop table register_diff_annotations;
create table register_diff_annotations
as
select * from register_vs_annotations
where register_label <> label;

alter table register_diff_annotations
add constraint pk_register_diff_annotations primary key (id);

CREATE INDEX "register_diff_annotations_tile_geom_index" ON "register_diff_annotations" USING gist (tile_geom);





