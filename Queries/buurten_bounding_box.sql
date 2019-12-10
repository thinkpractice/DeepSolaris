-- BB ZL_HR
select * from buurt_2017
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), wkb_geometry);
-- BB Heerlen
select * from buurt_2017
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), wkb_geometry);
--Whole ZL
select * from buurt_2017 
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
and bu_code = 'BU08990337';

create index pv_2017_nl_geom_idx
on pv_2017_nl
using GIST (location);
--Solar panels in ZL
select * from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), location);

-- Solar panels in ZL BB
select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(181300, 327600, 190600, 314500, 28992), location);
-- Solar panels in Heerlen BB
select count(*) from pv_2017_nl
where ST_Contains(ST_MakeEnvelope(190700, 327600, 200000, 314500, 28992), location);

-- Number of solar panels per "buurt" in Zuid Limburg
select bu_code, bu_naam, wk_code, gm_naam, count(pv_id) as num_solar_panels, wkb_geometry from buurt_2017 as bu
left join pv_2017_nl as pv on ST_Contains(wkb_geometry, location)
where ST_Contains(ST_MakeEnvelope(172700, 306800, 205000,  338400, 28992), wkb_geometry)
group by bu_code, bu_naam, wk_code, gm_naam, wkb_geometry
having count(pv_id) = 0;