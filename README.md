# Dagster Data Pipeline – Shopflow Project

## Project Overview

This project implements an end-to-end data pipeline using **Dagster**. The pipeline ingests raw order data, performs validation and cleaning, generates summary metrics, and enriches records by joining with product data.

The goal of this project is to demonstrate core data engineering concepts such as asset-based workflows, dependency management, data validation, aggregation, and multi-source joins.

---

## Tech Stack

- **Python**
- **Dagster** (data orchestration)
- **CSV files** (data sources)
- **Git & GitHub**

---

## Pipeline Architecture

The pipeline is built using Dagster assets and follows a modular, dependency-driven design:

- `raw_orders` → loads raw order data  
- `cleaned_orders` → validates and cleans data  
- `order_summary` → generates summary metrics  
- `raw_products` → loads product dataset  
- `enriched_orders` → joins orders with product data  

Dagster automatically manages execution order based on dependencies.

---

## Data Flow

```
raw_orders → cleaned_orders → order_summary
                ↓
          enriched_orders ← raw_products
```

---

## Key Features

- Data validation and cleaning for real-world messy datasets  
- Dependency-driven pipeline using Dagster assets  
- Aggregation of business metrics (revenue, order counts)  
- Multi-source data joining (orders + products)  
- Modular and reusable pipeline design  

---

## Example Output

### Order Summary

```python
{
  "total_orders": 16,
  "total_revenue": ...,
  "orders_by_status": {
    "delivered": 8,
    "shipped": 4,
    "pending": 3,
    "cancelled": 1
  }
}
```

### Enriched Orders

```python
{
  "order_id": 1,
  "product_id": 3,
  "product_name": "Headphones",
  "category": "Electronics",
  ...
}
```

---

## Setup Instructions

### 1. Scaffold the project

```bash
uvx create-dagster@latest shopflow
cd shopflow
```

### 2. Install dependencies

```bash
uv sync
source .venv/bin/activate
```

### 3. Add data

Create a `data/` folder and add:

- `orders.csv`
- `products.csv`

---

### 4. Run Dagster

```bash
dg dev
```

Open:

```
http://localhost:3000
```

---

## What This Project Demonstrates

- Building data pipelines using Dagster  
- Designing asset-based workflows  
- Cleaning and validating data  
- Performing aggregations  
- Joining multiple datasets  
- Debugging real-world pipeline issues  

---

## Author

**Toyor12**
