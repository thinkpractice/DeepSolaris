drop table register_label_per_building;
create table register_label_per_building
as 
(
	select *, 
		case when pv.pv_id is not null then 1 else 0 end as register_label	
	from areaofinterest as ai
	inner join bagactueel.pand as pa on ST_Intersects(pa.geovlak, ai.area)
	left join pv_2017_nl as pv on ST_Contains(pa.geovlak, pv.location)
	where ai.area_id = 19 or ai.area_id = 23 and 
	pa.aanduidingrecordinactief = false and pa.einddatumtijdvakgeldigheid is null and
	(pa.pandstatus <> 'Pand gesloopt'::bagactueel.pandstatus and 
	pa.pandstatus <> 'Bouwvergunning verleend'::bagactueel.pandstatus and 
	pa.pandstatus <> 'Niet gerealiseerd pand'::bagactueel.pandstatus)
);