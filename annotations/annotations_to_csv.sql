copy ( 
	select d.id, d.name, i.uuid, count(distinct(iu."imageID")) as count, 
		sum(case when iu.annotation = 1 then 1 else 0 end) as positives, 
		sum(case when iu.annotation = 0 then 1 else 0 end) as negatives, 
		sum(case when iu.annotation = -1 then 1 else 0 end) as dkn, 
		min(at.annotation) as annotation_tim 
	from "Image_User" as iu
	inner join "Image" as i on i.id = iu."imageID"
	inner join "Dataset" as d on d.id = i."datasetID"
	inner join 
		(select "imageID", "annotation" from "Image_User" where "userID" = 1) at
		on iu."imageID" = at."imageID"
	group by d.id, iu."imageID", i.uuid
	order by d.id, iu."imageID"

) to '/tmp/deepsolaris_annotations28082019.csv' with csv delimiter ';';
