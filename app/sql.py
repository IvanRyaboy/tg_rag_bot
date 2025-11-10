SQL_APARTMENTS = """
SELECT 
  a.id::text AS id,
  a.title, a.price, a.total_area, a.living_area, a.kitchen_area, a.balcony_area,
  a.balcony, a.room_count, a.description, a.floor, a.sale_conditions, a.bathroom_count,
  a.ceiling_height, a.renovation, a.condition,
  a.level_count, a.ownership_type, a.link,
  b.floors_total, b.wall_material, b.construction_year, b.house_amenities, b.parking,
  l.district, l.microdistrict, l.street, l.house_number, l.latitude, l.longitude,
  t.name AS town, r.name AS region
FROM apartments_apartment a
JOIN apartments_building b  ON b.id = a.building_id
JOIN apartments_location l  ON l.id = b.location_id
JOIN apartments_town t      ON t.id = l.town_id
JOIN apartments_region r    ON r.id = t.region_id
WHERE a.id = ANY(%s)
ORDER BY a.id;
"""

SQL_RENT = """
SELECT 
  a.id::text AS id,
  a.title, a.price, a.total_area, a.living_area, a.kitchen_area, a.term_of_rent,
  a.balcony, a.room_count, a.description, a.floor, a.rent_conditions, a.separate_rooms,
  a.renovation, a.level_count, a.ownership_type, a.link,
  b.floors_total, b.wall_material, b.construction_year, b.house_amenities, b.parking,
  l.district, l.microdistrict, l.street, l.house_number, l.latitude, l.longitude,
  t.name AS town, r.name AS region
FROM apartments_apartment a
JOIN apartments_building b  ON b.id = a.building_id
JOIN apartments_location l  ON l.id = b.location_id
JOIN apartments_town t      ON t.id = l.town_id
JOIN apartments_region r    ON r.id = t.region_id
WHERE a.id = ANY(%s)
ORDER BY a.id;
"""
