# Product Catalog API — Homework 02

In-memory FastAPI product catalog extending the Session 01 example with `in_stock` availability and filtering. Data is stored in memory and resets when the server restarts.

## Run

From the repository root:

```sh
.venv/bin/python -m pip install -r lectures/week-01/code/requirements.txt
.venv/bin/python -m uvicorn main:app --app-dir student-work/odildusmurodovv/week-01/catalog --reload
```

Open `http://127.0.0.1:8000/docs` to test the endpoints.

## Omitted vs. `false`

- **`GET /products` (`in_stock` omitted / `None`):** No stock filter is applied, so both available (`true`) and unavailable (`false`) products are returned.
- **`GET /products?in_stock=false`:** Filtered explicitly with `if in_stock is not None:`, returning only unavailable products. Writing `if in_stock:` would skip the filter for `false` and behave as if the parameter were omitted.
- **`POST /products`:** Omitting `in_stock` defaults it to `true` in `ProductCreate`, while passing `"in_stock": false` preserves `false`.

## Evidence (tested via `/docs`)

| Check | Request | Observed status | Response summary |
| :--- | :--- | :--- | :--- |
| Create without `in_stock` | `POST /products` with `{"name": "Notebook", "price": 5, "category": "stationery"}` | `201` | `{"id": 4, "name": "Notebook", "price": 5.0, "category": "stationery", "in_stock": true}` |
| Create with `in_stock=false` | `POST /products` with `{"name": "Desk Lamp", "price": 20, "category": "electronics", "in_stock": false}` | `201` | `{"id": 5, "name": "Desk Lamp", "price": 20.0, "category": "electronics", "in_stock": false}` |
| List without stock filter | `GET /products` | `200` | Returns all products, including both `in_stock: true` and `in_stock: false` |
| Filter `in_stock=false` | `GET /products?in_stock=false` | `200` | Returns only unavailable products (`"in_stock": false`, IDs `3` and `5`) |
| Filter `category` and `in_stock` | `GET /products?category=books&in_stock=true` | `200` | Returns only `[{"id": 1, "name": "Python Handbook", "price": 25.0, "category": "books", "in_stock": true}]` |
| `POST` empty name | `POST /products` with `{"name": "", "price": 5, "category": "books"}` | `422` | Validation error on `name`; no product created |

## Blockers

None.
