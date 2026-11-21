# Verified server quality receipts — 17 November 2026

## B2BLife

[PR2](https://github.com/teyfikoz/B2BLife/pull/2) and
[PR3](https://github.com/teyfikoz/B2BLife/pull/3) merged; final merge05c5d07.
Global last-report leakage replaced by session-owned opaque references, seven-day
snapshots, exact paid delivery and free export limit50. Webhooks fail closed and
validate fresh Paddle signatures; payment logs no longer include customer email.

Production inspection found legacy user data still in SQLite. It was privately
backed up and **not migrated**. New snapshots use a separate local Hetzner
PostgreSQL database/role; no production SQLite fallback. Dedicated PG metadata is
isolated from legacy initialization. Daily purge installed. Twenty-eight scoped
synthetic tests and full GitHub CI pass; real scoped PG owner-isolation smoke
passed and synthetic rows were removed. Public health200 and anonymous exports400.

Known limits: legacy DB migration and durable idempotent fulfillment/retry queue
remain separate work. Never interpret webhook200 alone as successful delivery.

## HomeLab

[PR2](https://github.com/teyfikoz/homelab/pull/2) and
[PR3](https://github.com/teyfikoz/homelab/pull/3) merged. Complete73-asset offline
snapshot deployed atomically; old root and hashed assets preserved. Existing tabs
keep their matching worker until normal activation. Health/biometric records stay
on device. Nginx health API proxy removed: `/api` and `/api/interpret` return403.
Public shell/guard/worker/inventory200; CSPconnect-srcnone, SW/inventoryno-cache.
Seventeen Node cases, TypeScript, Vite and Node18/20/22 CI pass. Actual device
first-install/airplane-mode QA is still separate; no such claim is made here.

## KredimPlus and TSA

[KrediPR2](https://github.com/teyfikoz/kredimplus/pull/2) merged1ee4095 and
[TSAPR2](https://github.com/teyfikoz/Tech-Sync-Analytica-LLC/pull/2) merged6d4ec0b.
Five activation/failure/rollback fixture checks passed for each. First real
production attempts safely failed on full disk, preserving active releases.
After reviewed recovery, Actions43796547442 and43796553563 attempt2 succeeded.
Fresh HTTPS healthz responses returned exact merged SHAs and statusok. Alerts were
not disabled or hidden. Healthz is artifact/liveness proof, not exhaustive QA.

## SciBreak / capacity

See [bounded render guard](scibreak-render-safety/README.md). Shared gates pause new
collections/rendering below5.5GiB. Historical valid archives were preserved and no
new public broadcast started. More storage or explicit archive policy is needed.

No secret values, DSNs, customer reports or health records are included in this
receipt. Unrelated dirty checkouts were preserved. NotebookLM topic sources were
updated for B2B, Kredi, TSA, operations and SaaS Ecosystem.
