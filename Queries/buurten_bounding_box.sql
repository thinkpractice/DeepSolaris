-- Assign tiles to neighbourhood
drop table neigbourhood_to_tile;
create table neighbourhood_to_tile
as
select *, 
	ST_Area(ST_Intersection(ti.area, bu.wkb_geometry)) / ST_Area(ti.area) as area_fraction_in_neighbourhood
from buurt_2017 as bu
inner join tiles as ti on ST_Intersects(bu.wkb_geometry, ti.area)
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), bu.wkb_geometry) 
and (area_id = 19 or area_id = 21);

-- Assign tiles to neighbourhood
drop table neigbourhood_to_building;
create table neigbourhood_to_building
as
select pa.*, 
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_code, bu.gm_naam,
	ST_Area(ST_Intersection(pa.geovlak, bu.wkb_geometry)) / ST_Area(pa.geovlak) as area_fraction_in_neighbourhood
from buurt_2017 as bu
inner join register_label_per_building as pa on ST_Intersects(bu.wkb_geometry, pa.geovlak)
where 
	ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), bu.wkb_geometry);

-- Create weighing table for annotations
drop table weighted_annotations_per_nb;
create table weighted_annotations_per_nb
as 
select 
	ag.*,  
	nt.bu_code, nt.bu_naam, nt.wk_code, nt.gm_code, nt.gm_naam, nt.area_fraction_in_neighbourhood,
	ag.label * nt.area_fraction_in_neighbourhood as weighted_label 
from annotations_per_tile_geo as ag
inner join neighbourhood_to_tile as nt on nt.tile_id = ag.tile_id;

alter table weighted_annotations_per_nb
add constraint pk_weighted_annotations_per_nb
primary key (bu_code, tile_id);

select * from weighted_annotations_per_nb
order by tile_id;

-- Number of annotations/annotated solar panels per neighbourhood in Zuid Limburg
select 
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
	count(id) as num_annotations, 
	sum(
		case when 
			label < 0 
		then 0 
		else coalesce(weighted_label, 0) 
		end
	) as num_solar_panels_annotations, 
	wkb_geometry 
from buurt_2017 as bu
left join weighted_annotations_per_nb as wa on bu.bu_code = wa.bu_code
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, wkb_geometry;

-- Create weighing table for model predictions
drop table model_predictions_geo;
create table model_predictions_geo
as
select mp.*, ti.tile_id, ti.area_id, ti.area as tile_geom
from model_predictions as mp
inner join tiles as ti on ti.uuid = mp.uuid;

alter table model_predictions_geo
add constraint pk_model_predictions_geo 
primary key  (tile_id);

create index model_predictions_geo_idx
on model_predictions_geo
using gist(tile_geom);

select distinct(area_id) 
from model_predictions_geo;

drop table weighted_predictions_per_nb;
create table weighted_predictions_per_nb
as 
select 
	mp.*,  
	nt.bu_code, nt.bu_naam, nt.wk_code, nt.gm_code, nt.gm_naam, nt.area_fraction_in_neighbourhood,
	mp.label * nt.area_fraction_in_neighbourhood as weighted_label 
from model_predictions_geo as mp
inner join neighbourhood_to_tile as nt on nt.tile_id = mp.tile_id;

alter table weighted_predictions_per_nb
add constraint pk_weighted_predictions_per_nb
primary key (bu_code, tile_id);

select * from weighted_predictions_per_nb
order by tile_id;

-- Model predictions per neighbourhood
select 
	mp.area_id,
	sum(case when at.label = 1 and at.label = mp.label then 1 else 0 end) as positives,
	sum(case when at.label = 0 and mp.label = 1 then 1 else 0 end) as false_positives,
	sum(case when at.label = 0 and at.label = mp.label then 1 else 0 end) as negatives,
	sum(case when at.label = 1 and mp.label = 0 then 1 else 0 end) as false_negatives,
	sum(case when at.label = 1 then 1 else 0 end) as num_positives,
	sum(case when at.label = 0 then 1 else 0 end) as num_negatives,
	count(*) as total
from annotations_per_tile_geo as at
inner join model_predictions_geo as mp on at.uuid = UUID(mp.uuid)
where at.label <> -1
group by mp.area_id
order by mp.area_id;

select
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
	count(*) as num_predictions, 
	sum(
		case when 
			label < 0 
		then 0 
		else coalesce(weighted_label, 0) 
		end
	) as num_solar_panels_predictions, 
	wkb_geometry 
from buurt_2017 as bu
left join weighted_predictions_per_nb as wp on bu.bu_code = wp.bu_code
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, wkb_geometry;

-- Create weighing table for register labels per neighbourhood
drop table weighted_register_labels_per_nb;
create table weighted_register_labels_per_nb
as 
select 
	*,
	register_label * area_fraction_in_neighbourhood as weighted_label 
from neigbourhood_to_building;

select count(*)
from bagactueel.pandactueel as pa
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), pa.geovlak);

-- Number of annotations BB Heerlen
select count(*) from annotations_per_tile_geo
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), tile_geom);

select count(*) from annotations_per_tile_geo
where ST_Intersects(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), tile_geom);

-- Number of annotations ZL_HR
select count(*) from annotations_per_tile_geo
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), tile_geom);

select count(*) from annotations_per_tile_geo
where ST_Intersects(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), tile_geom);

-- Number of model predictions
select count(*) from model_predictions;

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




--neighbourhood_to_tile
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu_code, bu_naam, wk_code, gm_naam, wkb_geometry;

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


 

