# Promotion checklist — before making repositories public

## Engineering
- [x] Original archive types inspected and private model inventory created
- [x] Six public-safe independent project folders created
- [x] SQLite synthetic schemas, views, and data generator built for four BI projects
- [x] Offline daily/weekly archive simulations and tests created
- [x] SQL and Python suite passes (see `python -m unittest discover -s tests -v`)
- [ ] Every DAX measure tested in Power BI on the matching synthetic schema
- [ ] Every Power Query M snippet tested in Power BI Desktop on the synthetic inputs
- [ ] Public mock PBIP reports built and visually compared against actual screenshots
- [ ] Source-to-reconstruction equivalence review approved by the employer if required

## Security and publication
- [ ] Written clearance for public description/case study of employer work where required
- [ ] Source code history, sample files, screenshots, and diagrams checked for secrets/metadata
- [ ] Every uploaded dashboard screenshot reviewed at full resolution
- [ ] Any vendor data license reviewed; only synthetic/authorized examples in release
- [ ] Previously committed public API keys revoked/rotated; history issue resolved
- [ ] Private source-reference archive permanently excluded from public Git

## Recruiter experience
- [ ] GitHub profile README points to high-signal public repositories
- [ ] Project cover screenshots show fictional data clearly marked as illustrative
- [ ] README reproductions run from a clean clone without credentials
- [ ] One measured result or reliable design decision described per project
- [ ] Resume bullet claims verified and differentiated from planned work
