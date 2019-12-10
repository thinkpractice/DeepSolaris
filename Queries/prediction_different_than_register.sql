'create table prediction_different_than_register
as'

select pp.pandid as pp_pandid, pp.model_label, pp.register_label, pa.* from predictions_per_building as pp
inner join bagactueel.pand as pa on pp.pandid = pa.identificatie
where model_label <> register_label
limit 100;
