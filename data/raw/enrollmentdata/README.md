# BVSD Enrollment Dashboard

An interactive map of enrollment, building capacity, and the Resilient Schools
consolidation process in the Boulder Valley School District (BVSD), Colorado.

**Live site:** https://enrollmentdata.org

A non-partisan, non-profit community project by [Yoav Lurie](https://yoavlurie.com).
It is **not affiliated with or endorsed by BVSD**. All figures come from BVSD's
published materials; see the [About page](https://enrollmentdata.org/about/) for a
full bibliography of sources and what each was used for.

## What's on the map

- Per-school enrollment 2014–2025 (BVSD October headcount) with 10-year peaks and trends
- Building capacity and 5-year enrollment projections (elementary and middle levels,
  from BVSD's Feb 2026 Annual Enrollment Trend Report and Oct 2025 Board worksession)
- BVSD's Aug 25, 2026 Resilient Schools proposal: closures, consolidations,
  reconfigurations and relocations, with movement arrows and post-change projections
- Color modes: % of 10-year peak, % of capacity (today / 2030 status quo / 2030 with
  proposal), projected change, and the proposed plan
- Attendance-area boundary overlays and a district overview with what the proposal
  does — and doesn't — resolve

## Running locally

Everything is static HTML/JS in `maps/` (no build step). Serve it with:

```bash
node maps/serve.js 8080
```

then open http://localhost:8080. `maps/index.html` and `maps/bvsd-enrollment-map.html`
are identical copies (keep them in sync when editing).

## License

This project is dedicated to the public domain under [CC0 1.0](LICENSE). Use it for
anything, commercial or not, with or without attribution.

Notes for reusers:

- The underlying enrollment and capacity figures are facts from public BVSD Board
  materials; the CC0 dedication covers this project's code, design, and data
  transcriptions.
- Map rendering uses [Leaflet](https://leafletjs.com) (BSD-2, loaded from CDN);
  basemap tiles are served by Esri with underlying data © OpenStreetMap
  contributors, under their own terms.
- Attendance-area boundaries derive from BVSD's public GIS layers.
