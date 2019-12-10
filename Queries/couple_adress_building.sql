select count(*) from bagactueel.adres_full;
select count(*) from bagactueel.pand; 

select 
	a.openbareruimtenaam, a.huisnummer, a.huisletter, a.huisnummertoevoeging, a.postcode, a.woonplaatsnaam, 
	a.gemeentenaam, a.provincienaam, a.verblijfsobjectgebruiksdoel, a.oppervlakteverblijfsobject, a.verblijfsobjectstatus,
	a.typeadresseerbaarobject, a.pandid, a.pandstatus as a_pandstatus, a.pandbouwjaar, a.nummeraanduiding, a.nevenadres,
	a.geopunt, a.textsearchable_adres, a.gid as a_gid,
	
	p.gid as p_gid, p.identificatie, p.aanduidingrecordinactief, p.aanduidingrecordcorrectie, p.officieel,  
	p.inonderzoek, p.begindatumtijdvakgeldigheid, p.einddatumtijdvakgeldigheid, p.documentnummer, p.documentdatum, 
	p.pandstatus as p_pandstatus, p.bouwjaar, p.geom_valid, p.geovlak
into pand_adres 
from bagactueel.adres_full as a
inner join bagactueel.pand as p on p.identificatie = a.pandid;