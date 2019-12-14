select * from neigbourhood_to_tile
limit 100;

select count(distinct(tile_id))
from neighbourhood_to_tile
where area_fraction_in_neighbourhood < 1.0
order by tile_id, area_fraction_in_neighbourhood desc;

select distinct(uuid) from tiles
group by uuid
having count(*) > 1


select count(distinct(tile_id))
from neighbourhood_to_tile
where area_fraction_in_neighbourhood < 1;

-- Some tiles are on the boundary of the bounding box, they appear only once in the count (second) query, but
-- they have area_fraction_in_neighbourhood < 1, so they appear in the area fraction (first) query too.
-- There are 435 tiles that are considered this way. The area_fraction_in_neighbourhood is therefore calculated
-- correctly and can be use to weigh the results.
select distinct(bu_naam) from neighbourhood_to_tile as nt
inner join
(
	select distinct(tile_id)
	from neighbourhood_to_tile
	where area_fraction_in_neighbourhood < 1
except
	select distinct(tile_id) from neighbourhood_to_tile
	group by tile_id
	having count(*) > 1
) diff on diff.tile_id = nt.tile_id
order by area_fraction_in_neighbourhood desc;

select count(*) from tiles
where area_id = 19 or area_id = 21;