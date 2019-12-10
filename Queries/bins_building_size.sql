select count(*) from bagactueel.pand
where aanduidingrecordinactief = false and einddatumtijdvakgeldigheid is null;
order by  ST_Area(geovlak) desc;

with pand_stats as (
	select min(ST_Area(geovlak)) as min,
           max(ST_Area(geovlak)) as max
	from bagactueel.pand
	where aanduidingrecordinactief = false;
),
histogram as (
	select width_bucket(ST_Area(geovlak), min, max, 199) as bucket,
		numrange(cast(min(ST_Area(geovlak)) as numeric), cast(max(ST_Area(geovlak)) as numeric), '[]') as range,
		count(*) as freq
	    from bagactueel.pand, pand_stats
	    where aanduidingrecordinactief = false;
	group by bucket
	order by bucket
)   
select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
from histogram;




