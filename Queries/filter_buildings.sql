select count(*) from bagactueel.pand
where aanduidingrecordinactief = false and einddatumtijdvakgeldigheid is null and
(pandstatus <> 'Pand gesloopt'::bagactueel.pandstatus and 
pandstatus <> 'Bouwvergunning verleend'::bagactueel.pandstatus and 
pandstatus <> 'Niet gerealiseerd pand'::bagactueel.pandstatus);

--begindatumtijdvakgeldigheid