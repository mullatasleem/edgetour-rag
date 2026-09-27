# tourism_jeju.json — sources

Pulled 2026-09-26 for the EdgeTour-RAG project (Day 2 dataset).

## Composition (729 entries)
- **OpenStreetMap (709)** — tourism POIs in the Jeju bbox (33.05–33.60 N, 126.05–127.00 E,
  includes Udo/Gapado/Marado) via the Overpass API. Tags: tourism=attraction|museum|
  theme_park|viewpoint|zoo|aquarium|gallery|artwork, natural=beach|peak|cave_entrance.
  Real names, categories, coordinates, Korean names where mapped. Descriptions are thin
  (derived from tags) — this is the long tail.
- **Wikipedia (16)** — pages in "Tourist attractions in Jeju Province" with real intro
  descriptions (3–4 sentences), e.g. Seongsan Ilchulbong, Sanbangsan, Jeongbang Waterfall,
  Daepo Jusangjeolli Cliff, Jeju Olle Trail, Udo, Gotjawal. Junk category members
  (organization, convention center, elementary school, festival) filtered out.
- **Curated (4)** — 2 bus/transport notes + 2 seasonal weather notes (the plan asked for
  bus routes and weather notes; these are hand-written).

## Dedup
Canonical key = normalized name minus trailing generic words (peak, beach, museum, ...).
Wikipedia version wins on collision (richer description).

## Schema per entry
id, name, name_ko, category, subcategory, description, latitude, longitude, address, source

## License notes
- OpenStreetMap data: © OpenStreetMap contributors, ODbL.
- Wikipedia extracts: CC BY-SA.

## Enrichment pass — 2026-09-26 (overnight)
12 of the 709 OSM entries had their thin tag-derived descriptions replaced with real
2–4 sentence intros from the English Wikipedia API (action=query, prop=extracts, exintro),
trimmed to ~500 chars. Entries carry `"description_source": "wikipedia"`.
Method: 120 thin-description candidates ranked by name recognition were queried as
`<name> Jeju`; a description was used only if the top result's title clearly referred to
the same place (token-subset match) AND the article mentioned Jeju (guard waived only
for exact title matches). 108 candidates were skipped as ambiguous/no-article, and
5 initial matches were reverted on manual review (wrong article, e.g. a memoir titled
"The Glass Castle"; generic definitions not about the place). The 16 Wikipedia entries
and 4 curated notes were not touched. Backup of the pre-enrichment file:
`tourism_jeju.orig.json`. Enriched examples: Hyeopjae Beach, Cheonjiyeon Waterfall,
Manjanggul Lava Tube, Oedolgae Rock, Jeju Stone Park, Jusangjeolli, Jeju Loveland,
Hanwha Aqua Planet Jeju, Sinchang Windmill Coastal Road, Jeju Haenyeo Museum,
Geomunoreum (crater viewpoint), Manjanggul Lava Tube Entrance.
Wikipedia text used under CC BY-SA; attribution: Wikipedia contributors.
