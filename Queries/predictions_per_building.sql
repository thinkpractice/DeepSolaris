create table predictions_per_building
as
select 	pandid, 
	max(model_label) as model_label, 
	max(register_label) as register_label,
	sum(model_label) as model_tiles_label_one,
	sum(case when model_label = 0 then 1 else 0 end) as model_tiles_label_zero,
	sum(register_label) as register_label_one,
	sum(case when register_label = 0 then 1 else 0 end) as register_label_zero
from register_vs_predictions
group by pandid;

 