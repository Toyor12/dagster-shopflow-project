🇬🇧 [English](README.md) | 🇩🇪 [Deutsch](README_DE.md)

# Day 2 — Afternoon Lab
## Assets, Dependencies, and I/O

### Learning Objectives

By the end of this lab you will be able to:

- **Scaffold** a new Dagster project from scratch (recall from Day 1)
- **Define** assets with explicit return type annotations
- **Chain** assets using dependency declarations
- **Clean and validate** real-world messy data inside an asset
- **Aggregate** data across assets and verify results in Dagit
- **Join** multiple data sources within a multi-input asset

---

## Setup

Before starting the exercises, scaffold a fresh project and prepare the data.

### Step 1 — Scaffold the Project

Create a new Dagster project named **`shopflow`** inside this directory. Refer to your Day 1 notes or the [Dagster docs](https://docs.dagster.io) if you need a reminder of the scaffolding command.

> **Hint:** You used a `uvx create-dagster@latest ...` command on Day 1.

After scaffolding, `cd` into the `shopflow/` directory for all remaining steps.

### Step 2 — Install Dependencies

```bash
uv sync
source .venv/bin/activate
```

### Step 3 — Create the Data File

Create a `data/` directory at the project root (next to `src/`) and add a file called `orders.csv` with the following content:

```csv
order_id,customer_id,product_id,quantity,price,order_date,timestamp,status
1,1,3,1,129.99,2026-01-01,2026-01-01T08:15:00Z,delivered
2,5,11,2,79.98,2026-01-01,2026-01-01T09:30:00Z,delivered
3,2,7,1,49.99,2026-01-02,2026-01-02T10:00:00Z,shipped
4,8,1,3,59.97,2026-01-02,2026-01-02T14:20:00Z,pending
5,3,15,1,199.99,2026-01-03,2026-01-03T11:45:00Z,cancelled
6,1,9,2,39.98,2026-01-03,2026-01-03T16:00:00Z,delivered
7,6,4,1,89.99,2026-01-04,2026-01-04T08:30:00Z,shipped
8,4,12,1,149.99,2026-01-04,2026-01-04T12:10:00Z,delivered
9,7,2,4,119.96,2026-01-05,2026-01-05T09:00:00Z,pending
10,9,8,1,29.99,2026-01-05,2026-01-05T15:30:00Z,delivered
11,2,5,2,69.98,2026-01-06,2026-01-06T10:15:00Z,shipped
12,10,14,1,249.99,2026-01-06,2026-01-06T13:45:00Z,delivered
13,,6,1,59.99,2026-01-07,2026-01-07T08:00:00Z,delivered
14,5,10,2,99.98,2026-01-07,2026-01-07T11:30:00Z,
15,3,13,1,179.99,2026-01-08,2026-01-08T09:20:00Z,DELIVERED
16,8,1,0,0.00,2026-01-08,2026-01-08T14:00:00Z,pending
17,1,7,,44.99,2026-01-09,2026-01-09T10:00:00Z,shipped
18,6,3,2,259.98,2026-01-09,2026-01-09T16:30:00Z,delivered
19,4,11,1,79.99,2026-01-10,2026-01-10T08:45:00Z,returned
20,2,9,3,59.97,2026-01-10,2026-01-10T12:00:00Z,  Shipped
```

### Step 4 — Verify Your Setup

Start the dev server and confirm everything is wired up:

```bash
dg dev
```

Open Dagit at **http://localhost:3000**. You should see the default Dagster landing page with no errors. Once confirmed, stop the server (`Ctrl+C`) — you'll restart it as you work through the exercises.

### Step 5 — Create Your Working File

The scaffolded project has a `defs/` folder but no asset files yet. Create the file where all your asset code will go:

```
src/shopflow/defs/assets.py
```

Dagster auto-discovers assets from the `defs/` folder, so this file will be picked up automatically.

---

## Exercises

Complete **at least the Basic tier** before moving on. The Intermediate and Advanced tiers are stretch goals — tackle them if you finish early.

> **Reminder:** You'll need `from dagster import asset` and `import csv` at the top of `assets.py`. When Dagster runs your assets, the working directory is the **project root** (`shopflow/`), so `data/orders.csv` will resolve correctly as a relative path.

### 🟢 Basic

1. **Implement `raw_orders`**
   - Read `data/orders.csv` using Python's built-in `csv.DictReader`.
   - Return the data as a `list[dict]`.
   - Add the return type annotation `-> list[dict]`.
   - Materialize the asset in Dagit and confirm it succeeds.

2. **Implement `cleaned_orders`**
   - Declare the dependency on `raw_orders` using a function parameter with a type annotation.
   - Skip any row where a required field (`order_id`, `customer_id`, `product_id`, `quantity`, `price`, `order_date`, `status`) is empty.
   - Normalize the `status` field to lowercase and strip whitespace.
   - Skip rows whose status is not one of: `pending`, `shipped`, `delivered`, `cancelled`.
   - Convert `quantity` to `int` and `price` to `float`.
   - Return a new list of cleaned dictionaries — do not modify the original rows.

3. **Verify the graph**
   - Open the Asset Graph in Dagit. Confirm the arrow points from `raw_orders` to `cleaned_orders`.
   - Materialize both assets together. How many rows does `cleaned_orders` produce? Write the answer as a comment in your code.

4. **Inspect the dirty rows**
   - Look at `orders.csv` and identify which rows are dropped by your cleaning logic and why. Write a comment listing the row numbers and the reason each was removed (e.g., "row 13 — empty customer_id").

---

### 🔵 Intermediate

1. **Add `order_summary`**
   - Create a new asset that depends on `cleaned_orders`.
   - Return a dictionary with:
     - `total_orders`: the number of cleaned rows
     - `total_revenue`: the sum of `quantity * price` for all rows
     - `orders_by_status`: a dictionary mapping each status to its count (e.g., `{"delivered": 8, "shipped": 3, ...}`)
   - Add the return type annotation `-> dict`.
   - Materialize and verify the output makes sense given the CSV data.

2. **Test the dependency chain**
   - Materialize only `order_summary` without first materializing the upstream assets. What does Dagster do?
   - Now re-materialize only `raw_orders`. Check Dagit — are `cleaned_orders` and `order_summary` marked as stale? Why or why not?

3. **Explain I/O manager behavior**
   - In a comment at the top of `assets.py`, answer in 2–3 sentences: how does the value from `raw_orders` get passed to `cleaned_orders`? What I/O manager is being used, and where is the data stored?

4. **Classify these scenarios**
   - For each scenario below, state whether you would use an `@asset`, an `@op`, or a `define_asset_job()`, and explain why in one sentence:
     - (a) A table that aggregates daily website visits
     - (b) Sending an alert email when a pipeline step fails
     - (c) Running `raw_orders`, `cleaned_orders`, and `order_summary` on a schedule every morning

---

### 🟣 Advanced

1. **Add a second data source: `raw_products`**
   - Create a file `data/products.csv` with columns: `product_id`, `name`, `category`, `unit_price`. Include at least 10 rows.
   - Create a `raw_products` asset that reads this file and returns `list[dict]`.

2. **Build `enriched_orders`**
   - Create an asset that depends on **both** `cleaned_orders` and `raw_products`.
   - For each cleaned order, look up the matching product by `product_id` and add the product's `name` and `category` to the order dictionary.
   - If a product is not found, set `name` to `"Unknown"` and `category` to `"Unknown"`.
   - Return the enriched list.

3. **Analyze the asset graph**
   - Open the Asset Graph in Dagit. Sketch or describe the full graph shape — how many nodes, how many edges, and which assets can run in parallel?
   - Materialize everything. Then change one row in `products.csv` and re-materialize only `raw_products`. Which downstream assets does Dagit mark as stale?

4. **Dependency style decision**
   - Imagine that in Day 3 you will write `loaded_orders`, which inserts `cleaned_orders` data into a PostgreSQL table using custom SQL.
   - Would you declare the dependency using a function parameter or `deps`? Write 3–4 sentences justifying your choice, referencing how the data flows and what the I/O manager would (or would not) do.
