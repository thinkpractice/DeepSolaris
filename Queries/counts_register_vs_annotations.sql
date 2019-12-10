-- Solar Panels annotated differently than the register, check total area of solar panels in tile
select * from register_vs_annotations
where register_label = 1 and register_label <> label and label <> -1 and num_buildings = 1
order by min_intersection_area;

copy 
( 
	select 
		uuid, filename, dataset_name, num_positives, num_negatives, num_dkn, total_annotations, num_buildings, min_intersection_area, max_intersection_area 
	from register_vs_annotations
	where  register_label = 1 and register_label <> label and label <> -1
	order by uuid
)
to '/tmp/annotations_different_than_register.csv'
delimiter ';' csv header;

-- Solar Panels not in register, check whether these are in the aerial of 2017
select * from register_vs_annotations
where label = 1 and register_label <> label
order by id;

copy 
( 
	select 
		uuid, filename, dataset_name, num_positives, num_negatives, num_dkn, total_annotations, num_buildings, min_intersection_area, max_intersection_area  
	from register_vs_annotations
	where label = 1 and register_label <> label
	order by uuid
)
to '/tmp/new_solar_panels.csv'
delimiter ';' csv header;

-- Total amount of differences between register and annotations
select count(*) from register_vs_annotations
where register_label <> label;

-- Total amount of similar labels
select count(*) from register_vs_annotations
where register_label = label;

-- Total amount of similar positive labels
select count(*) from register_vs_annotations
where register_label = label and label = 1;

-- Amount of annotations with only one annotator
select count(*) from register_vs_annotations
where total_annotations = 1;