create table annotations_per_tile
(
	id int not null,
	uuid uuid,
	uuid_str varchar not null,
	filename varchar,
	default_annotation int,
	num_positives int,
	num_negatives int,
	num_dkn int,
	total_annotations int,
	dataset_name varchar,
		
	constraint annotations_per_tile_pkey primary key(id)
);

copy annotations_per_tile(id, uuid_str, filename, default_annotation, num_positives, num_negatives, num_dkn, total_annotations, dataset_name)
from '/tmp/annotations201120191618.csv'
delimiter ';' header csv; 

update annotations_per_tile
set uuid = UUID(uuid_str);
create unique index uuid_idx ON annotations_per_tile (uuid);

alter table annotations_per_tile drop column uuid_str;

alter table annotations_per_tile add column label int;

create table temp_uuid_label
as
(select
    uuid,
    case 
	when num_positives >= num_negatives and num_positives > num_dkn then 1
	when num_negatives >= num_positives and num_negatives > num_dkn then 0
	else -1
    end	as label	
from annotations_per_tile)

update annotations_per_tile 
set label = a.label
from (select * from temp_uuid_label) a
where annotations_per_tile.uuid = a.uuid 

