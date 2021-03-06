--Create a table with selected neighbourhoods
drop table selected_neighbourhoods;
create table selected_neighbourhoods
as
select 
	bu.*
from buurt_2017 as bu
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), bu.wkb_geometry);

alter table selected_neighbourhoods
add column in_train_set boolean;

alter table selected_neighbourhoods
add column in_validation_set boolean;

alter table selected_neighbourhoods
add column in_train_validation_set boolean;

update selected_neighbourhoods
set in_train_set = ST_Intersects(wkb_geometry, ai.area)
from areaofinterest as ai
where ai.area_id = 19 and ST_Intersects(wkb_geometry, ai.area);

update selected_neighbourhoods
set in_validation_set = ST_Intersects(wkb_geometry, ai.area)
from areaofinterest as ai
where ai.area_id = 23 and ST_Intersects(wkb_geometry, ai.area);

update selected_neighbourhoods
set in_train_validation_set = in_train_set or in_validation_set;

--Create a table with selected buildings?

-- Assign tiles to neighbourhood
drop table neighbourhood_to_tile;
create table neighbourhood_to_tile
as
select *, 
	ST_Area(ST_Intersection(ti.area, bu.wkb_geometry)) / ST_Area(ti.area) as area_fraction_in_neighbourhood
from selected_neighbourhoods as bu
inner join tiles as ti on ST_Intersects(bu.wkb_geometry, ti.area)
where in_train_validation_set = true;

select count(*) from neighbourhood_to_tile;
-- Assign buildings to neighbourhood
drop table register_label_per_building;
create table register_label_per_building
as 
(
	select *, 
		case when pv.pv_id is not null then 1 else 0 end as register_label	
	from bagactueel.pand as pa 
	left join pv_2017_nl as pv on ST_Contains(pa.geovlak, pv.location)
	where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), pa.geovlak) and
	pa.aanduidingrecordinactief = false and pa.einddatumtijdvakgeldigheid is null and
	(pa.pandstatus <> 'Pand gesloopt'::bagactueel.pandstatus and 
	pa.pandstatus <> 'Bouwvergunning verleend'::bagactueel.pandstatus and 
	pa.pandstatus <> 'Niet gerealiseerd pand'::bagactueel.pandstatus)
);

drop table neigbourhood_to_building;
create table neigbourhood_to_building
as
select pa.*, 
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_code, bu.gm_naam,
	ST_Area(ST_Intersection(pa.geovlak, bu.wkb_geometry)) / ST_Area(pa.geovlak) as area_fraction_in_neighbourhood,
	bu.wkb_geometry
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

select count(*) from weighted_annotations_per_nb
order by tile_id;

-- Number of annotations/annotated solar panels per neighbourhood in Zuid Limburg
drop table weighted_annotations_aggr_nb;
create table weighted_annotations_aggr_nb
as
select 
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
	count(id) as num_annotations, 
	sum(
		case when 
			weighted_label < 0 
		then 0 
		else coalesce(weighted_label, 0) 
		end
	) as num_solar_panels_annotations, 
	wkb_geometry 
from buurt_2017 as bu
left join weighted_annotations_per_nb as wa on bu.bu_code = wa.bu_code
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, wkb_geometry;

select count(*) from weighted_annotations_aggr_nb;

-- Create weighing table for model predictions
drop table model_predictions;
create table model_predictions
(		
	uuid_string varchar(36),	
	prediction double precision,
	label int
);

copy model_predictions (uuid_string, prediction, label)
from '/media/tdjg/Data1/DeepSolaris/all_predictions.csv'
csv delimiter ';' header;

alter table model_predictions
add column prediction_id serial;

alter table model_predictions
add column uuid UUID;

alter table model_predictions
add column model_name varchar;

delete from model_predictions
where uuid_string like 'feh%';

update model_predictions
set uuid = UUID(uuid_string);

update model_predictions
set model_name = 'vgg16_best';


alter table model_predictions
drop column uuid_string;

-- delete double uuids...
select count(*)
from model_predictions
where uuid in
(
	select uuid from model_predictions
	group by uuid
	having count(uuid) > 1
);

select count(*) from model_predictions;

delete from model_predictions 
where prediction_id in
(
	select max(prediction_id) from model_predictions	
	group by uuid
	having count(uuid) > 1
);

alter table model_predictions
add constraint pk_model_predictions primary key (uuid, model_name);

drop table model_predictions_geo;
create table model_predictions_geo
as
select mp.*, ti.tile_id, ti.area_id, ti.area as tile_geom
from model_predictions as mp
inner join tiles as ti on UUID(ti.uuid) = mp.uuid;

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

drop table weighted_predictions_aggr_nb;
create table weighted_predictions_aggr_nb
as
select
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
	count(*) as num_predictions,
	sum(
		case when 
			weighted_label < 0 
		then 0 
		else coalesce(weighted_label, 0) 
		end
	) as num_solar_panels_predictions, 
	wkb_geometry 
from buurt_2017 as bu
left join weighted_predictions_per_nb as wp on bu.bu_code = wp.bu_code
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, wkb_geometry;

select count(*) from weighted_predictions_aggr_nb;

-- Create weighing table for register labels per neighbourhood


drop table weighted_register_labels_per_nb;
create table weighted_register_labels_per_nb
as 
select 
	*,
	register_label * area_fraction_in_neighbourhood as weighted_label 
from neigbourhood_to_building;

select count(distinct(bu_code)) from neigbourhood_to_building;

select building_id, area_fraction_in_neighbourhood, weighted_label 
from weighted_register_labels_per_nb
order by building_id;

select count(*)
from bagactueel.pandactueel as pa
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), pa.geovlak);

drop table weighted_register_labels_aggr_nb;
create table weighted_register_labels_aggr_nb
as
select 
	bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, 
	count(*) as num_register_labels, 
	sum(
		case when 
			weighted_label < 0 
		then 0 
		else coalesce(weighted_label, 0) 
		end
	) as num_solar_panels_register, 
	wkb_geometry 
from weighted_register_labels_per_nb as bu
group by bu.bu_code, bu.bu_naam, bu.wk_code, bu.gm_naam, bu.wkb_geometry;

select count(*) from weighted_register_labels_aggr_nb;

-- Create diff tables per neighbourhood
-- We need differences between labels!! Not just in numbers.
-- should num_predictions, num_annotations, num_register_labels be weighted?
drop table weighted_diff_per_nb;
create table weighted_diff_per_nb
as
select wpa.bu_code, wpa.bu_naam, wpa.wk_code, wpa.gm_naam, 
		num_annotations,
		num_annotations / ST_Area(wpa.wkb_geometry) as num_annotations_norm,
		num_solar_panels_annotations,
		num_solar_panels_annotations / ST_Area(wpa.wkb_geometry) as num_solar_panels_annotations_norm, 
		num_predictions,
		num_predictions / ST_Area(wpa.wkb_geometry) as num_predictions_norm,
		num_solar_panels_predictions,
		num_solar_panels_predictions / ST_Area(wpa.wkb_geometry) as num_solar_panels_predictions_norm, 
		num_register_labels,
		num_register_labels / ST_Area(wpa.wkb_geometry) as num_register_labels_norm,
		num_solar_panels_register,		
		num_solar_panels_register / ST_Area(wpa.wkb_geometry) as num_solar_panels_register_norm,
		num_solar_panels_predictions - num_solar_panels_annotations as predictions_annotations_diff,
		(num_solar_panels_predictions - num_solar_panels_annotations) / ST_Area(wpa.wkb_geometry) as predictions_annotations_diff_norm,
		num_solar_panels_register - num_solar_panels_annotations as register_annotations_diff,
		(num_solar_panels_register - num_solar_panels_annotations) / ST_Area(wpa.wkb_geometry) as register_annotations_diff_norm,
		num_solar_panels_register - num_solar_panels_predictions as register_predictions_diff,
		(num_solar_panels_register - num_solar_panels_predictions) / ST_Area(wpa.wkb_geometry) as register_predictions_diff_norm,
		wpa.wkb_geometry		
from weighted_predictions_aggr_nb as wpa
inner join weighted_annotations_aggr_nb as waa on waa.bu_code = wpa.bu_code
inner join weighted_register_labels_aggr_nb as wra on wra.bu_code = wpa.bu_code;

select count(*) from weighted_diff_per_nb;		

select * from weighted_diff_per_nb
limit 100;
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


 

