-- BB ZL_HR
select * from buurt_2017
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), wkb_geometry);
-- BB Heerlen
select * from buurt_2017
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), wkb_geometry);
--Whole ZL
select * from buurt_2017 
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
and bu_code = 'BU08990337';

create index pv_2017_nl_geom_idx
on pv_2017_nl
using GIST (location);
--Solar panels in ZL
select * from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), location);

-- Solar panels in ZL BB
select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), location);
-- Solar panels in Heerlen BB
select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), location);

-- Number of solar panels per neighbourhood in Zuid Limburg
select bu_code, bu_naam, wk_code, gm_naam, count(pv_id) as num_solar_panels, wkb_geometry from buurt_2017 as bu
left join pv_2017_nl as pv on ST_Contains(wkb_geometry, location)
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu_code, bu_naam, wk_code, gm_naam, wkb_geometry
having count(pv_id) = 0;

-- Unique register entries
select count(distinct(bag_address_id)) from buurt_2017 as bu
inner join pv_2017_nl as pv on ST_Contains(wkb_geometry, location)
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry);



-- Number of annotations/annotated solar panels per neighbourhood in Zuid Limburg
select 
	bu_code, bu_naam, wk_code, gm_naam, 
	count(id) as num_annotations, 
	sum(
		case when 
			label = -1 
		then 0 
		else coalesce(label, 0) 
		end
	) as num_solar_panels_annotations, 
	wkb_geometry 
from buurt_2017 as bu
left join annotations_per_tile_geo as pv on ST_Contains(wkb_geometry, tile_geom)
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu_code, bu_naam, wk_code, gm_naam, wkb_geometry;

-- Model predictions per neighbourhood
drop table predictions_per_tile;
create table predictions_per_tile
as
(
    select mp.*, ti.tile_id, ti.tile_geom from model_predictions as mp
    inner join tiles as ti on mp.uuid = ti.uuid
    where ti.area_id = 19 or ti.area_id = 21;
);

alter table predictions_per_tile
add primary key ();

create index predictions_per_tile_geo_idx
on predictions_per_tile
using gist(tile_geom);

drop table predictions_per_bu;
create table predictions_per_bu
as
(
    select * from predictions_per_tile;
);


-- Combined: number of solar panels from register, number of annotations/annotated solar panels, difference between register and annotations per buurt
drop table num_solar_panels_bu_ann_vs_reg;
create table num_solar_panels_bu_ann_vs_reg
as
(
	select 
		bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
		min(spb.num_solar_panels) as num_solar_panels_register,
		count(distinct(an.id)) as num_annotations, 
		sum(
			case when 
				an.label = -1 
			then 0 
			else coalesce(an.label, 0) 
			end
		) as num_solar_panels_annotations, 
		bu.wkb_geometry 
	from buurt_2017 as bu
	inner join annotations_per_tile_geo as an on ST_Contains(bu.wkb_geometry, an.tile_geom)
	inner join
	(
		select bu_code, bu_naam, wk_code, gm_naam, count(pv_id) as num_solar_panels, wkb_geometry from buurt_2017 as bu
		left join pv_2017_nl as pv on ST_Contains(wkb_geometry, location)
		where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
		group by bu_code, bu_naam, wk_code, gm_naam, wkb_geometry
	) spb on spb.bu_code = bu.bu_code
	where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), bu.wkb_geometry) 
	group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, bu.wkb_geometry
);

-- Compare number of solar panels/annotations with original tables --> find missing values
select 
	sum(num_solar_panels_register) as total_solar_panels_register,
	sum(num_solar_panels_annotations) as total_solar_panels_annotations
from num_solar_panels_bu_ann_vs_reg;

select sum(label) from annotations_per_tile_geo;

select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), location);
-- Solar panels in Heerlen BB
select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), location);




