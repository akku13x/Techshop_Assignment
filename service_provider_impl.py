import pyodbc
from dao.service_provider import ServiceProvider
from entity.model.order import Order
from entity.model.order_detail import OrderDetail
from entity.model.payment import Payment
from exception.order_not_found import OrderNotFound

class ServiceProviderImpl(ServiceProvider):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def _get_connection(self):
        return pyodbc.connect(self.connection_string)

    def add_customer(self, customer):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES (?, ?, ?, ?, ?)",
                               (customer.first_name, customer.last_name, customer.email, customer.phone, customer.address))
                conn.commit()
                print("Customer added successfully.")
        except Exception as e:
            print(f"Error adding customer: {e}")

    def add_product(self, product):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Products (ProductName, Description, Price, StockQuantity) VALUES (?, ?, ?, ?)",
                               (product.product_name, product.description, product.price, product.stock_quantity))
                conn.commit()
                print("Product added successfully.")
        except Exception as e:
            print(f"Error adding product: {e}")

    def place_order(self, order: Order, order_details: list):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                if not all([order.customer_id, order.order_date, order.total_amount]):
                    print("Order is missing required attributes.")
                    return

                cursor.execute(""" 
                    INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) 
                    VALUES (?, ?, ?) 
                """, (order.customer_id, order.order_date, order.total_amount))

                order_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

                if order_id is None:
                    print("")
                    return

                print(f"Retrieved OrderID: {order_id}")

                for detail in order_details:
                    if not detail.product_id or detail.quantity <= 0:
                        print(f"Invalid order detail: {detail}")
                        continue
                    cursor.execute(""" 
                        INSERT INTO OrderDetails (OrderID, ProductID, Quantity) 
                        VALUES (?, ?, ?) 
                    """, (order_id, detail.product_id, detail.quantity))

                conn.commit()
                print("Order placed successfully.")
        except Exception as e:
            print(f"Error placing order: {e}")

    def get_product_price(self, product_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Price FROM Products WHERE ProductID = ?", (product_id,))
                price = cursor.fetchone()
                return price[0] if price else None
        except Exception as e:
            print(f"Error fetching product price: {e}")
            return None

    def update_product_quantity(self, product_id, new_quantity):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Products SET StockQuantity = ? WHERE ProductID = ?", (new_quantity, product_id))
                conn.commit()
                print("Product quantity updated successfully.")
        except Exception as e:
            print(f"Error updating product quantity: {e}")

    def get_order_status(self, order_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Status FROM Orders WHERE OrderID = ?", (order_id,))
                status = cursor.fetchone()
                return status[0] if status else None
        except Exception as e:
            print(f"Error fetching order status: {e}")
            return None

    def track_order_status(self, order_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Status FROM Orders WHERE OrderID = ?", (order_id,))
                status = cursor.fetchone()
                if status:
                    print(f"Order Status for Order ID {order_id}: {status[0]}")
                else:
                    print(f"No order found with Order ID {order_id}.")
        except Exception as e:
            print(f"Error tracking order status: {e}")

    def generate_sales_report(self, start_date, end_date):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT
                        Orders.OrderID,
                        Orders.OrderDate,
                        SUM(OrderDetails.Quantity * Products.Price) AS TotalSales,
                        COUNT(Orders.OrderID) AS NumberOfOrders
                    FROM
                        Orders
                    JOIN
                        OrderDetails ON Orders.OrderID = OrderDetails.OrderID
                    JOIN
                        Products ON OrderDetails.ProductID = Products.ProductID
                    WHERE
                        Orders.OrderDate BETWEEN ? AND ?
                    GROUP BY
                        Orders.OrderID, Orders.OrderDate
                """
                cursor.execute(query, (start_date, end_date))
                sales_data = cursor.fetchall()

                if sales_data:
                    print("Sales Report:")
                    print(f"{'Order ID':<10} {'Order Date':<20} {'Total Sales':<15} {'Number of Orders':<15}")
                    for row in sales_data:
                        print(f"{row.OrderID:<10} {row.OrderDate:<20} {row.TotalSales:<15} {row.NumberOfOrders:<15}")
                else:
                    print("No sales data found for the specified date range.")

        except Exception as e:
            print(f"Error generating sales report: {e}")

    def update_customer_info(self, customer_id, email=None, phone=None):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                query = "UPDATE Customers SET"
                params = []

                if email:
                    query += " Email = ?"
                    params.append(email)
                if phone:
                    query += ", Phone = ?"
                    params.append(phone)

                query += " WHERE CustomerID = ?"
                params.append(customer_id)

                cursor.execute(query, params)
                conn.commit()

                if cursor.rowcount > 0:
                    print("Customer information updated successfully.")
                else:
                    print("No customer found with the given ID.")
        except Exception as e:
            print(f"Error updating customer information: {e}")

    def process_payment(self, payment: Payment):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Payments (OrderID, PaymentMethod, Amount, PaymentDate) "
                    "VALUES (?, ?, ?, ?)",
                    (payment.get_order_id(), payment.get_payment_method(), payment.get_amount(), payment.get_payment_date())
                )
                conn.commit()
                print("Payment processed successfully.")
        except pyodbc.Error as e:
            raise Exception(f"Error processing payment: {e}")

    def search_products_by_category(self, category):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Products WHERE Category = ?", (category,))
                products = cursor.fetchall()
                return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return None

    def delete_product(self, product_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Products WHERE ProductID = ?", (product_id,))
                if cursor.rowcount == 0:
                    raise Exception("Product not found.")
                conn.commit()
        except Exception as e:
            print(f"Error deleting product: {e}")
            raise

    def list_customers(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Customers")
                customers = cursor.fetchall()
                return customers  # Return the list of customers
        except Exception as e:
            print(f"Error retrieving customers: {e}")
            return None

    def get_order_total(self, customer_id, order_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" 
                    SELECT TotalAmount FROM Orders 
                    WHERE CustomerID = ? AND OrderID = ?
                """, (customer_id, order_id))
                result = cursor.fetchone()
                if result:
                    return result[0]  # TotalAmount
                else:
                    raise OrderNotFound(f"No such order found for the given customer ID: {customer_id} and order ID: {order_id}.")
        except Exception as e:
            print(f"Error retrieving order total: {e}")
            raise
