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
- SQLite (local development simplicity)


## Architecture Decisions

###  Wallet ID
UUID is used as the primary key to avoid predictable identifiers and to reflect production-grade API design.

###  Balance Strategy
The wallet stores a `balance` field for efficient reads.  
Balance updates are protected using:

- `transaction.atomic()`
- `select_for_update()` row-level locking

This prevents race conditions during concurrent credits.


## Setup Instructions
1️⃣ Clone Repository
git clone <your-repo-url>
cd credit_wallet

2️⃣ Create Virtual Environment
python -m venv myenv


Activate:
Windows:
myenv\Scripts\activate

Mac/Linux:
source myenv/bin/activate

3️⃣ Install Dependencies

If using requirements file:
pip install -r requirements.txt


Or manually:
pip install django djangorestframework

4️⃣ Apply Migrations
python manage.py migrate

5️⃣ Run Development Server
python manage.py runserver


Server runs at:
http://127.0.0.1:8000/

Running Tests
python manage.py test
