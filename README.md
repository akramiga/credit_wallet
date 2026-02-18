# Wallet Credit Service

## Overview

This service implements a minimal wallet credit system using an append-only ledger model.

It supports:
- Crediting a wallet
- Idempotent credit operations
- Atomic transaction safety
- Basic RBAC guard (header-based)

The ledger is append-only and enforces data integrity at the database level.

---

## Tech Stack

- Django — mature ORM & transaction management
- Django REST Framework — clean API layer


PostgreSQL was chosen to ensure proper transactional integrity and database-level idempotency constraints.

---

## Architecture Decisions

### 1. Wallet ID
UUID is used as the primary key to avoid predictable identifiers and to reflect production-grade API design.

### 2. Balance Strategy
The wallet stores a `balance` field for efficient reads.  
Balance updates are protected using:

- `transaction.atomic()`
- `select_for_update()` row-level locking

This prevents race conditions during concurrent credits.

### 3. Idempotency
Idempotency is enforced at the database level via:

Unique constraint:
