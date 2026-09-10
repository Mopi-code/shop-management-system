# Shop Management System

A desktop shop/inventory management app built with **Python (Tkinter)** and **MySQL**. It lets you track products, record purchases, monitor stock, and flag expired food items — all through a simple GUI.

## Features

- Add, modify, and delete products (name, price, kind, amount, valid date, size)
- Buy products — automatically updates stock, total sales count, and total revenue
- View a separate purchases list with search and delete
- Search and sort products by any column
- Flag expired products (checks valid date against today for "Food" items)
- Import/export product data as CSV
- Light/dark theme toggle
- Bulk delete all data (with confirmation)

## Tech Stack

- **GUI:** Tkinter + tkcalendar (for date pickers)
- **Database:** MySQL
- **Connector:** mysql-connector-python

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up the database

Run the SQL script in `shop_project.sql` against your MySQL server. This creates the `shop` database along with the `products`, `purchases`, and `my_variables` tables:

```bash
mysql -u root -p < shop_project.sql
```

### 3. Configure your database credentials

Copy `.env.example` to `.env` and fill in your own MySQL credentials:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=shop
```

The `.env` file is git-ignored, so your real credentials never get committed.

### 4. Run the app

```bash
python shop_project.py
```

## Notes

- Dates are stored as text in `mm/dd/yy` format.
- The "expired products" check only applies to items with `kind = 'Food'`.
- This project was built as a learning project to practice GUI development and database integration in Python — feedback and suggestions are welcome!

## License

MIT
