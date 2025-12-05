# SaaS Template
A boilerplate Django + DRF project with user management, multi-tenancy, and subscription billing.
<br>

## Features
* User Registration & Login (JWT)
* Email verification
* Password reset
* Organizations / Teams (multi-tenancy)
* User roles: Owner, Admin, Member
* Stripe subscription billing (mock)
* Audit logs
<br>

## Requirements
* Python 3.11+
* Django 4.2+
* Django REST Framework (DRF)
* PostgreSQL 
* Docker & Docker Compose
<br>

## Installation
1. **Clone the repo**
```
git clone https://github.com/stantejada/saas-template-api.git
cd saas-template-api
```

2. **Start docker**
```
docker-compose up --build
```

3. **Apply migrations**
```
docker-compose exec web python manage.py migrate
```

4. **Create superuser**
```
docker-compose exec web python manage.py createsuperuser
```
<br>

## Endpoints
**Auth**
| Method | Endpoint                            | Description            |
| ------ | ----------------------------------- | ---------------------- |
| POST   | `/api/auth/register/`               | Register a new user    |
| GET    | `/api/auth/verify-email/?token=...` | Verify user email      |
| POST   | `/api/auth/forgot-password/`        | Request password reset |
| POST   | `/api/auth/reset-password/`         | Reset password         |
| POST   | `/api/token/`                       | Obtain JWT             |
| POST   | `/api/token/refresh/`               | Refresh JWT            |

**Profile**
| Method        | Endpoint        | Description              |
| ------------- | --------------- | ------------------------ |
| GET/PUT/PATCH | `/api/profile/` | View/update user profile |

**Organizations & Team**
| Method               | Endpoint                   | Description                   |
| -------------------- | -------------------------- | ----------------------------- |
| GET/POST             | `/api/organizations/`      | List / Create organizations   |
| GET/PUT/PATCH/DELETE | `/api/organizations/{id}/` | Retrieve, update, delete org  |
| GET/POST             | `/api/teams/`              | List / Create teams           |
| GET/PUT/PATCH/DELETE | `/api/teams/{id}/`         | Retrieve, update, delete team |
| GET/POST             | `/api/memberships/`        | List / Add members to teams   |
| GET/PUT/PATCH/DELETE | `/api/memberships/{id}/`   | Update / remove member        |

**Billing (Mock Stripe)**
| Method | Endpoint                                | Description                  |
| ------ | --------------------------------------- | ---------------------------- |
| POST   | `/api/billing/create-checkout-session/` | Simulate checkout            |
| POST   | `/api/billing/confirm-payment/`         | Confirm subscription payment |

**Audit Logs**
| Method | Endpoint                 | Description                        |
| ------ | ------------------------ | ---------------------------------- |
| GET    | `/api/audit/audit-logs/` | View audit logs for your org/teams |

<br>

## Usage

**Example Flow (Postman/API)**
Register User
POST /api/auth/register/ with:
```
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123"
}
```
<br>

## Permissions
* Only organization owners can edit or delete an org
* team admins/owners can manage team members
* Members can view but not modify teams/orgs
* Subscriptions are per organization

<br>

## Notes
* Email verification & password reset tokens are printed to console (dev mode).
* Billing is mocked; no real payments are processed.
* Audit logs record all CRUD actions on organizations, teams, memberships, and subscriptions.