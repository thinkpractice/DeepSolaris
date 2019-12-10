copy
(select i."id", i."uuid", 
	min(i."filename") as filename, 
	min(i."defaultAnnotation") as default_annotation,	
	sum(case when iu."annotation" = 1 then 1 else 0 end) as positives,
	sum(case when iu."annotation" = 0 then 1 else 0 end) as negatives,
	sum(case when iu."annotation" = -1 then 1 else 0 end) as dkn, 
	count(*) as total,
	min(d."name") as dataset_name
from "Image_User" as iu
inner join "Image" as i on iu."imageID" = i."id"
inner join "Dataset" as d on d."id" = i."datasetID"
group by i."id", i."uuid"
order by i."id", i."uuid")
to '/var/tmp/annotations201120191618.csv' delimiter ';' csv header;