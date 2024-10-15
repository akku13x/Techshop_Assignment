# Techshop - Assignment 1

## Project Structure
ecommerce_project/
│
├── entity/model/
│   ├── cart.py
│   ├── customer.py
│   ├── order.py
│   ├── order_item.py
│   └── product.py
│   └── __init__.py
│
├── dao/
│   ├── OrderProcessorRepository.py
│   └── service_provider_impl.py
│   └── __init__.py
│
├── exception/
│   ├── customernotfound.py
│   ├── ordernotfound.py
│   └── productnotfound.py
│   └── __init__.py
│
├── util/
│   ├── DBConnection.py
│   ├── PropertyUtil.py
│   └── db_connector.py
│   └── __init__.py
│
├── main/
|   └── mainmodule.py
│   └── __init__.py


## Technologies

--> Python: Backend logic and application structure.

--> MS SQL Server: Database for storing customers, products, orders, etc.

--> pyodbc: Python library for connecting to SQL Server.

-->Unit Testing: Testing framework for ensuring code quality.

### Author: Sarthak Niranjan Kulkarni
