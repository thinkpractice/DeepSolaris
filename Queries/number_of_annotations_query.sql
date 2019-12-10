copy
(
	select "uuid", count(distinct(iu."userID")) from "Image" as i
	inner join "Image_User" as iu on i.id = iu."imageID"
	group by "uuid"
	order by count(distinct(iu."userID"))
)
TO '/tmp/annotated_tiles.csv' delimiter ';' CSV HEADER;
