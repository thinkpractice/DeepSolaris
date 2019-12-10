create table register_vs_predictions as
select 
	pa.*, ti.tile_id, ti.uuid, ti.area, mp.label as model_label, 
	case 
		when pv.pv_id is not null then 1
		else 0
	end as register_label
from areaofinterest as ai
inner join pand_adres as pa on ST_Intersects(ai.area, pa.geovlak)
inner join tiles as ti on ST_Intersects(ti.area, pa.geovlak) and ti.area_id = ai.area_id
inner join model_predictions as mp on mp.uuid = ti.uuid
left join pv_2017_nl as pv on ST_Within(pv.location, pa.geovlak)
where ai.area_id = 19 
order by pa.a_gid;

'inner join annotated_tiles as at on at.uuid = ti.uuid
