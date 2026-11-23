# Publication and security controls

1. Only publish this reconstructed, synthetic package after reviewing its files and your employer's policies. Never copy the original archives, extracted source-reference bundle, production PBIX/PBIP files, vendor connection information, contract rates, identifiable loads, shipment data, real customer/carrier data, sensitive report screenshots, or secrets into public Git.
2. Employer source may be subject to intellectual-property and confidentiality restrictions even when all data rows are removed. Obtain written authorization for public code/data reproduction if required.
3. Synthetic means every identifier, shipment, rate, event, company, and measurement is invented for demonstration; do not use a “sanitized” production row with merely renamed identifiers.
4. Scan every candidate public file and all commit history with an appropriate secret scanner, check screenshots and metadata, verify licenses, and keep credentials in environment variables.
5. Previously committed API keys in another public repository must be revoked or rotated even after removing literals from the current branch. History requires separate attention.
6. M/DAX examples have not been executed in a Power BI engine; they require manual integration and verification against the synthetic model. SQL and Python examples are tested locally.
