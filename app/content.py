def apartment_content(row) -> str:
    parts = [
        f"Title: {row['title'] or 'Buy Apartment'}",
        f"Region: {row['region']}",
        f"Town: {row['town']}",
        f"District: {row['district'] or ''}",
        f"Microdistrict: {row['microdistrict'] or ''}",
        f"Street: {row['street'] or ''}",
        f"House: {row['house_number'] or ''}",
        f"Geo: lat={row['latitude'] or ''}, lon={row['longitude'] or ''}",
        (
            "Building: "
            f"floors_total={row['floors_total']}, "
            f"walls={row['wall_material'] or ''}, "
            f"year={row['construction_year'] or ''}, "
            f"parking={row['parking'] or ''}, "
            f"amenities={row['house_amenities'] or ''}"
        ),
        (
            "Apartment: "
            f"rooms={row['room_count']}, total_area={row['total_area']}, living_area={row['living_area']}, "
            f"kitchen_area={row['kitchen_area'] or ''}, balcony={row['balcony'] or ''}"
            f"({row['balcony_area'] or ''} m²), bathrooms={row['bathroom_count'] or ''}, "
            f"ceiling={row['ceiling_height'] or ''}, renovation={row['renovation'] or ''}, "
            f"condition={row['condition'] or ''}, sale={row['sale_conditions']}"
        ),
        f"Floor: {row['floor']}/{row['level_count'] or ''}",
        f"Ownership: {row['ownership_type']}",
        f"Price: {row['price']}",
        f"Link: {row['link'] or ''}",
        f"Description:\n{row['description'] or ''}".strip(),
    ]
    return "\n".join(parts)


def apartment_metadata(row) -> dict:
    return {
        "apartment_id": row["apartment_id"],
        "region": row["region"],
        "town": row["town"],
        "district": row["district"],
        "street": row["street"],
        "rooms": row["room_count"],
        "total_area": row["total_area"],
        "price": row["price"],
        "floor": row["floor"],
        "levels": row["level_count"],
        "condition": row["condition"],
        "sale": row["sale_conditions"],
        "ownership": row["ownership_type"],
        "year": row["construction_year"],
        "walls": row["wall_material"],
        "lat": row["latitude"],
        "lon": row["longitude"],
        "link": row["link"],
    }


def rent_content(row) -> str:
    apt_parking = row.get("apt_parking", row.get("parking"))
    bld_parking = row.get("building_parking")
    floors_total = row.get("floors_total")

    parts = [
        f"Title: {row.get('title') or 'Rent Apartment'}",
        f"Region: {row.get('region')}",
        f"Town: {row.get('town')}",
        f"District: {row.get('district') or ''}",
        f"Microdistrict: {row.get('microdistrict') or ''}",
        f"Street: {row.get('street') or ''}",
        f"House: {row.get('house_number') or ''}",
        f"Geo: lat={row.get('latitude') or ''}, lon={row.get('longitude') or ''}",
        (
            "Building: "
            f"floors_total={floors_total}, "
            f"walls={row.get('wall_material') or ''}, "
            f"year={row.get('construction_year') or ''}, "
            f"parking={bld_parking if bld_parking is not None else ''}, "
            f"amenities={row.get('house_amenities') or ''}"
        ),
        (
            "Apartment: "
            f"rooms={row.get('room_count')}, total_area={row.get('total_area')}, "
            f"living_area={row.get('living_area')}, "
            f"kitchen_area={row.get('kitchen_area') or ''}, balcony={row.get('balcony') or ''}, "
            f"separate_rooms={row.get('separate_rooms')}, "
            f"renovation={row.get('renovation') or ''}, "
            f"parking={apt_parking if apt_parking is not None else ''}, "
            f"rent_term={row.get('term_of_rent') or ''}, "
            f"rent_conditions={row.get('rent_conditions') or ''}"
        ),
        f"Floor: {row.get('floor')}/{row.get('level_count') or ''}",
        f"Ownership: {row.get('ownership_type')}",
        f"Price: {row.get('price')}",
        f"Link: {row.get('link') or ''}",
        ("Description:\n" + (row.get('description') or '')).strip(),
    ]
    return "\n".join(parts)


def rent_metadata(row) -> dict:
    apt_parking = row.get("apt_parking", row.get("parking"))
    bld_parking = row.get("building_parking")

    md = {
        "id": row.get("id"),
        "region": row.get("region"),
        "town": row.get("town"),
        "district": row.get("district"),
        "street": row.get("street"),
        "rooms": row.get("room_count"),
        "total_area": row.get("total_area"),
        "living_area": row.get("living_area"),
        "kitchen_area": row.get("kitchen_area"),
        "price": row.get("price"),
        "floor": row.get("floor"),
        "levels": row.get("level_count"),
        "ownership": row.get("ownership_type"),
        "year": row.get("construction_year"),
        "walls": row.get("wall_material"),
        "lat": row.get("latitude"),
        "lon": row.get("longitude"),
        "link": row.get("link"),
        "term_of_rent": row.get("term_of_rent"),
        "rent_conditions": row.get("rent_conditions"),
        "separate_rooms": row.get("separate_rooms"),
        "renovation": row.get("renovation"),
        "balcony": row.get("balcony"),
    }

    if bld_parking is not None:
        md["building_parking"] = bld_parking
    if apt_parking is not None:
        md["apartment_parking"] = apt_parking

    return md

