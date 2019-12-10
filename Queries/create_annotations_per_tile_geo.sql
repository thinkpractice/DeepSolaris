drop table annotations_per_tile_geo;
create table annotations_per_tile_geo
as
select at.*, ti.tile_id, ti.area as tile_geom, ti.area_id from annotations_per_tile as at
inner join tiles as ti on UUID(ti.uuid) = at.uuid;

alter table annotations_per_tile_geo 
add constraint pk_annotations_per_tile_geo primary key (id); 

CREATE INDEX "annotations_per_tile_geo_tile_geom_index" ON "annotations_per_tile_geo" USING gist (tile_geom);