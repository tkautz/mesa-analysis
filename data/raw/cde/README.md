# CDE pupil membership files — NOT RETRIEVED (2026-09-03)

Target: "PK-12 Membership Grade Level by School" XLSX for 2014-15 through 2025-26 from
https://www.cde.state.co.us/cdereval/rvprioryearpmdata and https://cde.state.co.us/cdereval/pupilcurrent,
plus any resident / non-resident (open enrollment) by-school file.

Result: both hosts are denied by this session's network egress policy.
- curl: `CONNECT tunnel failed, response 403` (see ../bvsd/FETCH_FAILURES.txt)
- WebFetch tool: `EGRESS_BLOCKED: Access to www.cde.state.co.us is blocked by the network egress proxy.`

Nothing in this directory is CDE data. See data/SOURCES.md for what to download by hand.
