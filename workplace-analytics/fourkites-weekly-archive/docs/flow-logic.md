# Weekly archive / workflow architecture

The supplied Power Automate flow export has a shared-mailbox event trigger and 27 named actions (including nested actions). It composes report date range and week start/end, filters **XLSX** attachments, constructs an archive filename, handles year/month folders, and creates or replaces files.

```mermaid
flowchart TD
 A[Shared mailbox event] --> B[Compose week range]
 B --> C[Filter XLSX attachments]
 C --> D{Eligible attachment?}
 D -- No --> Z[Terminate]
 D -- Yes --> E[Year/month folder check]
 E --> F[Retrieve attachment bytes]
 F --> G{Existing filename?}
 G -- Yes --> H[Replace]
 G -- No --> I[Create]
```

## Public implementation
The synthetic demonstration uses explicit week boundaries, verifies a seven-day inclusive window, prefixes the filename with the range and persists idempotently. The original flow's exact date parsing, URLs, and connection bindings remain private.

## Test cases
Wrong extensions; malformed ranges; year/month crossing; repeated attachments; replacement; no valid files. No claim is made that the original flow was deployed or ran error-free.
