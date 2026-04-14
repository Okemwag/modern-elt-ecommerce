#!/usr/bin/env python3
"""Generate deterministic, realistic sample e-commerce data.

The output is intentionally dependency-free so it can run in a clean Python
environment. It creates:

- CSV extracts for analysis and file-based ingestion
- CSV reference files used by the Airbyte file source
- A PostgreSQL seed script for the transactional source system
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


RANDOM_SEED = 20260414
CUSTOMER_COUNT = 2500
ORDER_COUNT = 9000
PRODUCT_COUNT = 260

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "generated"
CSV_DIR = ROOT / "csv"
SAMPLE_DIR = ROOT / "sample_data"
POSTGRES_INIT_DIR = ROOT.parent / "source_postgres" / "init"


FIRST_NAMES = [
    "Aisha", "Daniel", "Maya", "James", "Nina", "Omar", "Grace", "Liam",
    "Zoe", "Noah", "Ivy", "Ethan", "Chloe", "Lucas", "Mia", "Elijah",
    "Sofia", "Amara", "Kenji", "Fatima", "Mateo", "Priya", "Hannah",
    "David", "Imani", "Arjun", "Layla", "Samuel", "Nora", "Isaac",
]

LAST_NAMES = [
    "Okafor", "Smith", "Mwangi", "Patel", "Garcia", "Brown", "Kimani",
    "Chen", "Johnson", "Njoroge", "Williams", "Hassan", "Khan", "Lopez",
    "Nguyen", "Mensah", "Taylor", "Ali", "Singh", "Wilson", "Martinez",
    "Adebayo", "Robinson", "Miller", "Dlamini", "Karanja", "Davis",
]

BRANDS = [
    "Northline", "UrbanNest", "Kibo", "Luma", "Astra", "TerraForm",
    "BrightCart", "NovaWear", "PeakHome", "Everly", "FreshFold",
    "Mavuno", "BlueCove", "Atlas", "SokoWorks", "VividLoop",
]

CATEGORIES = [
    (1, "Electronics"),
    (2, "Home and Kitchen"),
    (3, "Fashion"),
    (4, "Beauty"),
    (5, "Sports"),
    (6, "Books"),
    (7, "Toys"),
    (8, "Grocery"),
    (9, "Office"),
    (10, "Pet Supplies"),
    (11, "Automotive"),
    (12, "Garden"),
]

REGIONS = [
    (1, "Nairobi Metro", "KE", ["Nairobi", "Kiambu", "Machakos"]),
    (2, "Coast Kenya", "KE", ["Mombasa", "Kilifi", "Malindi"]),
    (3, "Lagos Metro", "NG", ["Lagos", "Ikeja", "Lekki"]),
    (4, "Abuja Federal", "NG", ["Abuja", "Gwarinpa", "Wuse"]),
    (5, "Gauteng", "ZA", ["Johannesburg", "Pretoria", "Sandton"]),
    (6, "Western Cape", "ZA", ["Cape Town", "Stellenbosch", "George"]),
    (7, "California", "US", ["Los Angeles", "San Diego", "San Jose"]),
    (8, "New York", "US", ["New York", "Buffalo", "Albany"]),
    (9, "Texas", "US", ["Austin", "Dallas", "Houston"]),
    (10, "Ontario", "CA", ["Toronto", "Ottawa", "Hamilton"]),
    (11, "British Columbia", "CA", ["Vancouver", "Victoria", "Kelowna"]),
    (12, "England", "UK", ["London", "Manchester", "Birmingham"]),
    (13, "Bavaria", "DE", ["Munich", "Nuremberg", "Augsburg"]),
    (14, "Berlin", "DE", ["Berlin", "Potsdam", "Cottbus"]),
    (15, "New South Wales", "AU", ["Sydney", "Newcastle", "Wollongong"]),
    (16, "Victoria", "AU", ["Melbourne", "Geelong", "Ballarat"]),
]

PRODUCT_WORDS = [
    "Wireless", "Compact", "Premium", "Everyday", "Eco", "Smart", "Classic",
    "Travel", "Pro", "Essential", "Studio", "Outdoor", "Flex", "Lite",
    "Max", "Core", "Active", "Heritage", "Fresh", "Bold",
]

PRODUCT_NOUNS = {
    "Electronics": ["Headphones", "Charger", "Speaker", "Tablet Stand", "Keyboard"],
    "Home and Kitchen": ["Cookware Set", "Lamp", "Blender", "Storage Bin", "Mug Set"],
    "Fashion": ["Sneakers", "Jacket", "Backpack", "T-Shirt", "Watch"],
    "Beauty": ["Serum", "Moisturizer", "Cleanser", "Hair Dryer", "Sunscreen"],
    "Sports": ["Yoga Mat", "Water Bottle", "Training Shoes", "Dumbbell", "Gym Bag"],
    "Books": ["Planner", "Notebook", "Cookbook", "Guidebook", "Journal"],
    "Toys": ["Puzzle", "Building Set", "Board Game", "Doll", "RC Car"],
    "Grocery": ["Coffee Beans", "Tea Box", "Granola", "Olive Oil", "Snack Pack"],
    "Office": ["Desk Organizer", "Monitor Arm", "Mouse Pad", "Desk Chair", "Pen Set"],
    "Pet Supplies": ["Pet Bed", "Food Bowl", "Leash", "Cat Tree", "Treat Pack"],
    "Automotive": ["Car Vacuum", "Phone Mount", "Seat Cover", "Tool Kit", "Jump Starter"],
    "Garden": ["Planter", "Garden Hose", "Pruner", "Solar Light", "Seed Kit"],
}


def money(cents: int) -> str:
    return f"{cents / 100:.2f}"


def random_datetime(start: datetime, end: datetime) -> datetime:
    span_seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, span_seconds))


def weighted_status() -> str:
    statuses = [
        ("completed", 78),
        ("Complete", 6),
        ("SUCCESS", 4),
        ("pending", 5),
        ("cancelled", 4),
        ("returned", 3),
    ]
    return random.choices([s for s, _ in statuses], weights=[w for _, w in statuses], k=1)[0]


def normalized_order_status(status: str) -> str:
    value = status.lower()
    if value in {"completed", "complete", "success"}:
        return "completed"
    if value in {"cancelled", "canceled"}:
        return "cancelled"
    if value in {"returned", "return"}:
        return "returned"
    return "pending"


def payment_for_status(status: str) -> tuple[str, int]:
    if status == "completed":
        return random.choice(["paid", "PAID", "success"]), 1
    if status == "returned":
        return random.choice(["refunded", "refund"]), 1
    if status == "cancelled":
        return random.choice(["failed", "declined"]), 0
    return "pending", 0


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_value(value: object) -> str:
    if value is None:
        return r"\N"
    text = str(value)
    return text.replace("\\", "\\\\").replace("\t", " ").replace("\n", " ")


def write_copy_block(handle, table: str, columns: list[str], rows: list[dict]) -> None:
    handle.write(f"COPY {table} ({', '.join(columns)}) FROM stdin;\n")
    for row in rows:
        handle.write("\t".join(copy_value(row[column]) for column in columns))
        handle.write("\n")
    handle.write("\\.\n\n")


def build_regions() -> list[dict]:
    return [
        {"region_id": region_id, "region_name": region_name, "country": country}
        for region_id, region_name, country, _ in REGIONS
    ]


def build_customers() -> list[dict]:
    customers = []
    start = datetime(2022, 1, 1)
    end = datetime(2026, 3, 31)

    for customer_id in range(1, CUSTOMER_COUNT + 1):
        region_id, _, country, cities = random.choice(REGIONS)
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        email = f"{first_name}.{last_name}.{customer_id}@example.com".lower()
        created_at = random_datetime(start, end)

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": f"+{random.randint(1, 99)}{random.randint(100000000, 999999999)}",
                "city": random.choice(cities),
                "country": country,
                "created_at": created_at.isoformat(sep=" ", timespec="seconds"),
                "home_region_id": region_id,
            }
        )

    return customers


def build_products() -> tuple[list[dict], list[dict]]:
    categories = [
        {"category_id": category_id, "category_name": category_name}
        for category_id, category_name in CATEGORIES
    ]
    products = []

    for product_id in range(1, PRODUCT_COUNT + 1):
        category_id, category_name = random.choice(CATEGORIES)
        noun = random.choice(PRODUCT_NOUNS[category_name])
        adjective = random.choice(PRODUCT_WORDS)
        brand = random.choice(BRANDS)
        list_price_cents = random.randint(800, 45000)
        unit_cost_cents = int(list_price_cents * random.uniform(0.35, 0.72))

        products.append(
            {
                "product_id": product_id,
                "product_name": f"{adjective} {noun} {product_id}",
                "category_id": category_id,
                "brand": brand,
                "unit_cost": money(unit_cost_cents),
                "list_price": money(list_price_cents),
                "_list_price_cents": list_price_cents,
            }
        )

    return categories, products


def build_orders(customers: list[dict], products: list[dict]) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
    orders = []
    order_items = []
    payments = []
    returns = []
    shipping = []

    active_customer_ids = list(range(1, 2201))
    repeat_pool = random.choices(active_customer_ids, k=ORDER_COUNT - len(active_customer_ids))
    customer_sequence = active_customer_ids + repeat_pool
    random.shuffle(customer_sequence)

    start = datetime(2024, 1, 1)
    end = datetime(2026, 3, 31)
    item_id = 1
    payment_id = 1
    return_id = 1

    for order_id, customer_id in enumerate(customer_sequence, start=1):
        customer = customers[customer_id - 1]
        order_date = random_datetime(start, end)
        raw_status = weighted_status()
        status = normalized_order_status(raw_status)
        payment_status, successful_payment = payment_for_status(status)
        item_count = random.choices([1, 2, 3, 4, 5], weights=[35, 28, 20, 12, 5], k=1)[0]
        sampled_products = random.sample(products, item_count)
        order_total_cents = 0

        for product in sampled_products:
            quantity = random.choices([1, 2, 3, 4], weights=[65, 22, 10, 3], k=1)[0]
            base_price_cents = product["_list_price_cents"]
            unit_price_cents = int(base_price_cents * random.uniform(0.92, 1.05))
            gross_cents = quantity * unit_price_cents
            discount_rate = random.choices([0, 0.05, 0.10, 0.15], weights=[72, 15, 9, 4], k=1)[0]
            discount_cents = int(gross_cents * discount_rate)
            order_total_cents += gross_cents - discount_cents

            order_items.append(
                {
                    "order_item_id": item_id,
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": money(unit_price_cents),
                    "discount_amount": money(discount_cents),
                }
            )
            item_id += 1

        payment_amount_cents = order_total_cents if successful_payment else 0

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.isoformat(sep=" ", timespec="seconds"),
                "order_status": raw_status,
                "payment_status": payment_status,
                "shipping_region_id": customer["home_region_id"],
                "total_amount": money(order_total_cents),
            }
        )

        payments.append(
            {
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_method": random.choice(["card", "paypal", "bank_transfer", "mobile_money"]),
                "payment_status": payment_status,
                "payment_amount": money(payment_amount_cents),
                "paid_at": (order_date + timedelta(minutes=random.randint(1, 120))).isoformat(
                    sep=" ", timespec="seconds"
                ),
            }
        )
        payment_id += 1

        shipped_at = order_date + timedelta(hours=random.randint(4, 72))
        delivered_at = shipped_at + timedelta(days=random.randint(1, 8))
        shipping_status = {
            "completed": "delivered",
            "returned": "returned",
            "cancelled": "cancelled",
            "pending": "processing",
        }[status]
        shipping.append(
            {
                "shipment_id": order_id,
                "order_id": order_id,
                "shipping_provider": random.choice(["DHL", "FedEx", "UPS", "Sendy", "G4S"]),
                "shipping_status": shipping_status,
                "shipped_at": shipped_at.isoformat(sep=" ", timespec="seconds") if status != "cancelled" else "",
                "delivered_at": delivered_at.isoformat(sep=" ", timespec="seconds") if status in {"completed", "returned"} else "",
            }
        )

        if status == "returned" or (status == "completed" and random.random() < 0.025):
            returns.append(
                {
                    "return_id": return_id,
                    "order_id": order_id,
                    "return_reason": random.choice(["damaged", "wrong_size", "late_delivery", "changed_mind"]),
                    "return_status": random.choice(["received", "approved", "refunded"]),
                    "returned_at": (delivered_at + timedelta(days=random.randint(1, 21))).isoformat(
                        sep=" ", timespec="seconds"
                    ),
                    "refund_amount": money(int(order_total_cents * random.uniform(0.35, 1.0))),
                }
            )
            return_id += 1

    return orders, order_items, payments, returns, shipping


def build_inventory(products: list[dict]) -> list[dict]:
    inventory = []
    inventory_id = 1
    warehouse_regions = [1, 3, 5, 7, 10, 12, 15]

    for product in products:
        for region_id in random.sample(warehouse_regions, random.randint(2, 4)):
            inventory.append(
                {
                    "inventory_id": inventory_id,
                    "product_id": product["product_id"],
                    "warehouse_region_id": region_id,
                    "stock_quantity": random.randint(0, 900),
                    "reorder_threshold": random.randint(15, 120),
                    "last_stocked_at": random_datetime(datetime(2025, 1, 1), datetime(2026, 3, 31)).isoformat(
                        sep=" ", timespec="seconds"
                    ),
                }
            )
            inventory_id += 1

    return inventory


def write_postgres_seed(customers: list[dict], orders: list[dict], order_items: list[dict], payments: list[dict]) -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    seed_path = SAMPLE_DIR / "postgres_seed.sql"

    customer_cols = ["customer_id", "first_name", "last_name", "email", "phone", "city", "country", "created_at"]
    order_cols = ["order_id", "customer_id", "order_date", "order_status", "payment_status", "shipping_region_id", "total_amount"]
    item_cols = ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_amount"]
    payment_cols = ["payment_id", "order_id", "payment_method", "payment_status", "payment_amount", "paid_at"]

    with seed_path.open("w", encoding="utf-8") as handle:
        handle.write(
            """drop table if exists payments;
drop table if exists order_items;
drop table if exists orders;
drop table if exists customers;

create table customers (
    customer_id bigint primary key,
    first_name text not null,
    last_name text not null,
    email text not null,
    phone text,
    city text,
    country text,
    created_at timestamp not null
);

create table orders (
    order_id bigint primary key,
    customer_id bigint not null references customers(customer_id),
    order_date timestamp not null,
    order_status text not null,
    payment_status text not null,
    shipping_region_id bigint,
    total_amount numeric(18, 2) not null
);

create table order_items (
    order_item_id bigint primary key,
    order_id bigint not null references orders(order_id),
    product_id bigint not null,
    quantity integer not null,
    unit_price numeric(18, 2) not null,
    discount_amount numeric(18, 2) not null
);

create table payments (
    payment_id bigint primary key,
    order_id bigint not null references orders(order_id),
    payment_method text not null,
    payment_status text not null,
    payment_amount numeric(18, 2) not null,
    paid_at timestamp
);

"""
        )
        write_copy_block(handle, "customers", customer_cols, customers)
        write_copy_block(handle, "orders", order_cols, orders)
        write_copy_block(handle, "order_items", item_cols, order_items)
        write_copy_block(handle, "payments", payment_cols, payments)

    POSTGRES_INIT_DIR.mkdir(parents=True, exist_ok=True)
    init_path = POSTGRES_INIT_DIR / "01_seed.sql"
    init_path.write_text(seed_path.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> None:
    random.seed(RANDOM_SEED)

    customers = build_customers()
    categories, products = build_products()
    regions = build_regions()
    orders, order_items, payments, returns, shipping = build_orders(customers, products)
    inventory = build_inventory(products)

    product_rows = [{k: v for k, v in row.items() if not k.startswith("_")} for row in products]

    write_csv(GENERATED_DIR / "customers.csv", customers, list(customers[0].keys()))
    write_csv(GENERATED_DIR / "orders.csv", orders, list(orders[0].keys()))
    write_csv(GENERATED_DIR / "order_items.csv", order_items, list(order_items[0].keys()))
    write_csv(GENERATED_DIR / "payments.csv", payments, list(payments[0].keys()))
    write_csv(GENERATED_DIR / "products.csv", product_rows, list(product_rows[0].keys()))
    write_csv(GENERATED_DIR / "categories.csv", categories, list(categories[0].keys()))
    write_csv(GENERATED_DIR / "regions.csv", regions, list(regions[0].keys()))
    write_csv(GENERATED_DIR / "returns.csv", returns, list(returns[0].keys()))
    write_csv(GENERATED_DIR / "shipping.csv", shipping, list(shipping[0].keys()))
    write_csv(GENERATED_DIR / "inventory.csv", inventory, list(inventory[0].keys()))

    write_csv(CSV_DIR / "products.csv", product_rows, list(product_rows[0].keys()))
    write_csv(CSV_DIR / "categories.csv", categories, list(categories[0].keys()))
    write_csv(CSV_DIR / "regions.csv", regions, list(regions[0].keys()))

    write_postgres_seed(customers, orders, order_items, payments)

    print(f"customers: {len(customers)}")
    print(f"orders: {len(orders)}")
    print(f"order_items: {len(order_items)}")
    print(f"payments: {len(payments)}")
    print(f"products: {len(product_rows)}")
    print(f"categories: {len(categories)}")
    print(f"regions: {len(regions)}")
    print(f"returns: {len(returns)}")
    print(f"shipping: {len(shipping)}")
    print(f"inventory: {len(inventory)}")


if __name__ == "__main__":
    main()
