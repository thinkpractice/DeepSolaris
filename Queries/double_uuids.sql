select * from tiles
where UUID(uuid) in (
	select uuid from annotations_per_tile
	group by uuid
	having count(uuid) >= 2
);

select uuid, count(*) from tiles
group by uuid
having count(uuid) >= 2;



select * from tiles
where UUID(uuid) in (
	select uuid from annotations_per_tile 
	where dataset_name like 'ZL_%'
) and area_id = 19;


select * from tiles
where UUID(uuid) in (
	select uuid from annotations_per_tile 
	where dataset_name like 'Heerlen_%'
)
intersect
select * from tiles
where UUID(uuid) in (
	select uuid from annotations_per_tile 
	where dataset_name like 'ZL_%'
) and area_id = 19;

copy
(
	select * from tiles as ti
	inner join 
	(
		select * from annotations_per_tile 
		where dataset_name like 'ZL_%'
	) a 
	on UUID(ti.uuid) = a.uuid and ti.area_id = 19
)
to '/tmp/heerlen_tiles_in_zl_dataset.csv' csv delimiter ';' header;

select * from annotations_per_tile
where total_annotations = 1

delete from annotations_per_tile 
where uuid in 
(
	select UUID(ti.uuid) from tiles as ti
	inner join 
	(
		select * from annotations_per_tile 
		where dataset_name like 'ZL_%'
	) a 
	on UUID(ti.uuid) = a.uuid and ti.area_id = 19
)
