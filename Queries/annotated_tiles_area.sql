select ti.uuid, ti.area, at.number_annotations from tiles as ti 
inner join annotated_tiles as at on at.uuid = ti.uuid
where ti.area_id = 19;
