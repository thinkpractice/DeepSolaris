create table predictions_and_register_per_tile
as
(
	select 
		ti.uuid, 
		max(mp.label) as model_label, 
		case when count(pv.pv_id) > 0 then 1 else 0 end as register_label,
		ti.area 
	from tiles as ti
	inner join model_predictions as mp on ti.uuid = mp.uuid
	where ti.area_id = 19 or ti.area_id = 23	
	order by ti.uuid
);

