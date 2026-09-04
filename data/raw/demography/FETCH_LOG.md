# FETCH_LOG - public demographic data for the Mesa / Bear Creek analysis

Session date: 2026-09-03 (per-file UTC timestamps and md5s in `MANIFEST_demography.csv`).
All HTTP requests used User-Agent `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36`.
Nothing outside this directory was touched; every file here is new. Derived text siblings (`*.txt` next to a PDF, HTML or the DOCX
inside a zip) were produced with pdfplumber / tag-stripping; everything else is byte-for-byte as downloaded.

## 1. Boulder County births by year (priority 1) - OBTAINED from three independent publishers

| Publisher / series | File | Coverage | Period convention | How |
|---|---|---|---|---|
| SDO components of change, lookups API | `sdo_components_of_change_boulder_state_1970_2060.csv` (+ `_raw.json`) | 1970-2024 estimates, 2025-2060 projections; Boulder County and statewide | July-June year ending in the stated year (SDO estimates are as of July 1) | `https://gis.dola.colorado.gov/lookups/components?county=13&year=YYYY`, one request per year (91 x 2) |
| SDO components of change, bulk CSV | `sdo_bucket_components-change-county.csv` | 1970-2060, all 64 counties, Vintage 2024 (prepared March 2025) | same | `https://storage.googleapis.com/co-publicdata/components-change-county.csv`; values identical to the API series |
| Census Bureau county components (CO-EST) | `co-est2009-alldata.csv`, `co-est2020-alldata.csv`, `co-est2024-alldata.csv` | BIRTHS2000-2009, 2010-2020, 2020-2024 | July 1-June 30; the first year of each vintage is an April-June stub (BIRTHS2000, BIRTHS2010, BIRTHS2020) | www2.census.gov popest datasets |
| CDPHE Vital Statistics, via KIDS COUNT Data Center | `kidscount_aecf_live_births_by_county_colorado_ind9847.xlsx` | 1990-2024 calendar-year resident births, all CO counties (2021 absent from the export) | calendar year | `https://datacenter.aecf.org/rawdata.axd?ind=9847&loc=7` |
| CDPHE county summary tables 2025 | `cdphe_vital_statistics_boulder_county_summary_report_2025.xlsx`, sheet T6 | Total births 2015, 2021-2025 | calendar year | Google Drive folder linked from the CDPHE Vital Statistics Program page |

Boulder County births, side by side (SDO = Vintage 2024; Census = vintage shown; CDPHE = calendar year via KIDS COUNT, with 2021 and 2025 from CDPHE summary table T6):

| year | SDO (Jul-Jun) | Census v2009 | Census v2020 | Census v2024 | CDPHE (calendar) |
|---|---|---|---|---|---|
| 2000 | 3719 | 905* | | | 3864 |
| 2001 | 3402 | 3560 | | | 3933 |
| 2002 | 3575 | 3598 | | | 3656 |
| 2003 | 3636 | 3525 | | | 3620 |
| 2004 | 3571 | 3572 | | | 3548 |
| 2005 | 3510 | 3511 | | | 3500 |
| 2006 | 3511 | 3529 | | | 3407 |
| 2007 | 3390 | 3406 | | | 3461 |
| 2008 | 3353 | 3352 | | | 3215 |
| 2009 | 3187 | 3437 | | | 3235 |
| 2010 | 3141 | | 766* | | 3041 |
| 2011 | 2995 | | 2998 | | 2891 |
| 2012 | 2954 | | 2962 | | 3044 |
| 2013 | 2963 | | 2961 | | 2922 |
| 2014 | 2939 | | 2942 | | 2866 |
| 2015 | 2857 | | 2868 | | 2917 |
| 2016 | 2841 | | 2832 | | 2725 |
| 2017 | 2628 | | 2637 | | 2616 |
| 2018 | 2580 | | 2581 | | 2556 |
| 2019 | 2525 | | 2554 | | 2477 |
| 2020 | 2507 | | 2517 | 623* | 2427 |
| 2021 | 2472 | | | 2481 | 2545 (T6) |
| 2022 | 2430 | | | 2443 | 2420 |
| 2023 | 2398 | | | 2422 | 2291 |
| 2024 | 2304 | | | 2424 | 2418 |
| 2025 | 2351 (projection) | | | | 2465 (T6) |

`*` = April-June stub of a census year, not a full year.

Points to carry into `data/CONFLICTS.md` (that file was not edited here):
- SDO and Census county components agree to within ~1% for 2001-2022 (same July-June accounting). They diverge in 2023-2024 (SDO 2398 / 2304 vs Census 2422 / 2424).
- Calendar-year CDPHE counts differ from the July-June series by up to ~5% in single years, in both directions (2024: CDPHE 2418 vs SDO 2304 vs Census 2424). A rough test that SDO_y ~ (CDPHE_{y-1} + CDPHE_y) / 2 holds in 2005, 2010, 2016, 2018 and 2019 but not in 2020-2024, where SDO runs below the calendar data. For a births-to-kindergarten lag the calendar-year CDPHE series is the cleaner numerator (Colorado kindergarten cohorts are birth-date windows with an Oct 1 cut-off).
- SDO's projected 2025 births (2351) already sit ~5% below CDPHE's actual 2025 count (2465).
- KIDS COUNT 2019 Boulder = 2,477 matches the Colorado Children's Campaign 2021 county page; KIDS COUNT 2022-2024 match CDPHE T6 exactly, so the KIDS COUNT export is a faithful transcription of CDPHE.
- SDO's July-to-July accounting period is confirmed by the 2024 Colorado Population Summary, Figure 3 caption "Natural Change (Births Minus Deaths), July 2023 to July 2024" (`sdo_annual_population_summary_2024.txt`, line 99), and by the near-identity of the SDO and Census CO-EST series (Census documents its components as July 1-June 30). CDPHE / KIDS COUNT counts are calendar-year.

Did not work for births:
- `cohealthdata.dphe.state.co.us` (CoHID query tool and the historical county "Births and Deaths" PDFs such as `/chd/Resources/vs/2015/Boulder.pdf`): DNS did not resolve from this network for curl or WebFetch. `cohid.dphe.state.co.us`: same.
- `cdphe.colorado.gov/colorado-live-birth-statistics`: 403 to WebFetch, 200 to curl with browser UA; the page only links Tableau dashboards on `cohealthviz.dphe.state.co.us` (host reachable, but the `.csv` view-export URL returned 404 "missing-view"; a browser session would be needed).
- CDC WONDER natality: not attempted, because the WONDER API documentation states it does not serve sub-national (state/county) queries. County births can be pulled by hand in the web UI (Natality 2016-2024 expanded = D149; 2007-2023 = D66) as a fourth cross-check if wanted.
- data.colorado.gov (Socrata): a catalog search for "births" restricted to the Colorado domain returned no CDPHE births dataset (only SDO race layers and Census geography layers); federated hits such as `b3b6-bu6t` belong to other states.
- coepht.colorado.gov (Environmental Public Health Tracking): the live-birth page just embeds the same CoHID Tableau dashboard.

## 2. Births for City of Boulder / ZIP / tract (priority 2) - NOT OBTAINED from any public file

- No public file with sub-county resident births for Boulder was found. CDPHE's CoHID can query births by county and, in the web UI, by census tract / ZIP with small-cell suppression, but the host was unreachable here and the Tableau front-end has no export.
- Boulder County Public Health Community Health Assessment 2023 (`boulder_county_public_health_cha_2023.pdf`): contains no birth counts (checked; zero matches).
- Boulder County Health Compass (`bouldercountyhealthcompass.org`): DNS did not resolve.
- BVSD's Enrollment Dashboard (Tableau Public, workbook `BVSDEnrollmentDashboard`, sheets Welcome / Annual Trends / Enrollment Patterns / Gains-Losses / Home-Private School) shows "the number of births in the district" by region (press: North Boulder down ~250 births/yr vs 2006). Tableau Public metadata reports `allowDataAccess: false`, so the data cannot be downloaded programmatically; it may be readable by hand from the viz. The two BVSD news articles documenting the dashboard and the births statement are saved (`bvsd_news_*.html/.txt`).
- As a proxy, sub-county *age structure* was obtained: 2020 Census DHC P14 (single year of age under 20) at tract and block-group level, 2010 SF1 P14 at tract level, and ACS 2020-2024 B01001 at block-group level (section 5).

## 3. SDO single year of age, Boulder County (priority 3) - OBTAINED; City of Boulder age forecasts do not exist

- `sdo_bucket_sya-county.csv` (Vintage 2024, prepared March 2025): ages 0-100 x sex x county x year, 1990-2060; Estimate through 2024, Forecast 2025-2060. Boulder = `countyfips 13`. Read with `pd.read_csv(path, skiprows=1)`.
- Boulder County age 5 (SDO): 2010 3602, 2015 3441, 2020 3101, 2022 2720, 2023 2673, 2024 2642, 2025F 2665, 2027F 2608, 2030F 2573, 2035F 2696.
- The SDO API endpoint `https://gis.dola.colorado.gov/lookups/sya?county=13&year=YYYY` returned ECONNRESET on every attempt; the bulk CSV was used instead.
- City of Boulder: SDO publishes municipal *total* population only (`sdo_bucket_county-muni-timeseries.csv`, `sdo_bucket_muni-pop-housing.csv`; placefips 7850). SDO does not publish municipal or sub-county age estimates or forecasts; `forecast1yrsubstate.csv` is by planning region. For City of Boulder age structure use the Census extracts in section 5 (DHC 2020 P14, SF1 2010 P14, ACS 2020-2024 B01001 / B01002 / B11005 / B25003 at place level).
- Noted but not downloaded: `Blocks2020_Age_Selected_Categories.zip` (132 MB, SDO bucket; 2020 census-block age categories statewide). The block-group DHC extract covers the same need at a fraction of the size.

## 4. Births-to-kindergarten documentation (priority 4, optional)

- `casb_2025_state_demographer_school_age_population.pdf`: SDO deck to the Colorado Association of School Boards (fall 2025) - births falling / deaths rising, birth rates, school-age forecasts.
- `sdo_annual_population_summary_2023.pdf`, `_2024.pdf`: SDO narrative summaries (State Publications Library copies). The 2025 edition URL returned 404.
- `bvsd_news_enrollment_drops_more_than_expected_kindergarten_93pct_of_births.html`: BVSD statement that kindergarten entrants were 93% of births five years prior, two years running.
- No CDE statewide kindergarten-vs-births analysis was found; CDE's enrollment news releases attribute early-grade declines to SDO birth trends but publish no ratio.

## 5. ACS / Census small-area extracts (priority 5) - OBTAINED for all Boulder County tracts and block groups

- `api.census.gov` data queries now require an API key (HTTP 302 to `missing_key.html`, header `X-DataWebAPI-KeyError: 1`); no key is configured in this environment. Workaround: the `data.census.gov` table API (`https://data.census.gov/api/access/data/table?id=<TABLE>&g=<GEO>`) serves the same tables without a key. Exact URLs, row counts and timestamps: `census_acs5_2020_2024_tract_boulder_county_QUERY_URLS.csv`, `census_datacensusgov_subcounty_QUERY_URLS.csv`. Variable labels came from `api.census.gov/data/2024/acs/acs5/groups/<TABLE>.json` (label endpoints do not need a key).
- Tract level, ACS 2020-2024, all 78 Boulder County tracts: B01001 (sex by age, gives under-5 and 5-9), B01002 (median age), B09001 (population under 18 by age), B11005 (households with people under 18), B11003 (family type by presence of own children under 18), B25003 (tenure, gives owner-occupied share), B25008, B25010, B19013. Each as raw `.json` plus a verbatim `.csv`.
- Block-group level: ACS 2020-2024 B01001; 2020 DHC P12 and P14 (228 block groups).
- Tract level: 2020 DHC P14 and 2010 SF1 P14 (single year of age under 20; the 2010 rows use 2010 tract geography).
- Place level (Boulder city): ACS B01001 / B01002 / B11005 / B25003, DHC 2020 P14, SF1 2010 P14. County level: DHC 2020 P14, SF1 2010 P14.
- SDO's ACS 2020-2024 tract shapefile (`sdo_bucket_ACS2024_tract.zip`) carries 2020 tract geometry plus precomputed fields (`ageless10`, `age_0_9`, `ageless18`, `med_age`, `owned`, `rented`, `preschool`, `kndrgrtn`, `gr_1_4`, ...) and is the simplest layer to intersect with `data/raw/enrollmentdata/BVSD_Attendance_Areas.geojson`.
- Which tracts cover the Mesa / Bear Creek attendance areas was not determined here; all Boulder County tracts and block groups were pulled so the overlay can be done later without re-fetching.

## Tooling notes

- SDO public bucket listing: `https://storage.googleapis.com/co-publicdata/` (XML, 270 keys, not truncated). Other keys of possible later interest: `county_sya_race_estimates_current.csv` (42 MB), `race-estimates-county_current.csv`, `household-county.csv`, `srf_acs_tract.geojson`, `Blocks2020_Age_Selected_Categories.zip`.
- The SDO lookups API also exposes `https://gis.dola.colorado.gov/lookups/componentYRS` (year list used by the lookup pages).
- Census filenames `co-est*.csv` were kept as published so they match Census documentation; everything else is snake_case with a publisher prefix.
- `MANIFEST_demography.csv` has one row per file (md5, bytes, retrieval time); text siblings are marked as derived.
