import os
import sys
from datetime import datetime

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entity.model.customer import Customer
from entity.model.product import Product
from entity.model.order import Order
from entity.model.order_detail import OrderDetail
from entity.model.payment import Payment
from dao.service_provider_impl import ServiceProviderImpl
from util.db_property_util import DBPropertyUtil

def show_sales_report_menu(service_provider):
    print("Generate Sales Report")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    service_provider.generate_sales_report(start_date, end_date)

def update_customer_menu(service_provider):
    customer_id = int(input("Enter your Customer ID: "))
    email = input("Enter new email (leave blank to keep current): ")
    phone = input("Enter new phone number (leave blank to keep current): ")
    
    service_provider.update_customer_info(customer_id, email if email else None, phone if phone else None)

def process_payment(service_provider):
    print("Payment Processing")
    order_id = int(input("Enter the order ID: "))
    payment_method = input("Enter payment method (e.g., Credit Card, PayPal): ")
    amount = float(input("Enter payment amount: "))
    
    payment = Payment(order_id, payment_method, amount, datetime.now())
    try:
        service_provider.process_payment(payment)
        print("Payment processed successfully.")
    except Exception as e:
        print(f"Error processing payment: {e}")

def delete_product(service_provider):
    product_id = int(input("Enter product ID to delete: "))
    try:
        service_provider.delete_product(product_id)
        print("Product deleted successfully.")
    except Exception as e:
        print(f"Error deleting product: {e}")

def list_customers(service_provider):
    customers = service_provider.list_customers()
    if customers:
        print("List of Customers:")
        print(f"{'Customer ID':<12} {'First Name':<20} {'Last Name':<20} {'Email':<30} {'Phone':<15}")
        for customer in customers:
            print(f"{customer.CustomerID:<12} {customer.FirstName:<20} {customer.LastName:<20} {customer.Email:<30} {customer.Phone:<15}")
    else:
        print("No customers found.")

def show_order_total(service_provider):
    try:
        customer_id = int(input("Enter customer ID: "))
        order_id = int(input("Enter order ID: "))
        total_amount = service_provider.get_order_total(customer_id, order_id)
        if total_amount is not None:
            print(f"Total amount for order ID {order_id}: ${total_amount:.2f}")
        else:
            print("No such order found for the given customer ID.")
    except ValueError:
        print("Invalid input. Please enter valid customer ID and order ID.")

def display_menu():
    print("\n\n----- TechShop Menu -----\n")
    print("1. Add Customer")
    print("2. List Customers")
    print("3. Add Product")
    print("4. Place Order")
    print("5. Update Product Quantity")
    print("6. Track Order Status")
    print("7. Generate Sales Report")
    print("8. Update Customer Account")
    print("9. Payment Processing")
    print("10. Delete Product")
    print("11. Search Products by Category")
    print("12. Get Order Total")  # New option to get order total
    print("13. Exit")

def main():
    connection_string = DBPropertyUtil.get_connection_string()
    service_provider = ServiceProviderImpl(connection_string)
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            address = input("Enter address: ")
            customer = Customer(first_name, last_name, email, phone, address)
            service_provider.add_customer(customer)
            print("Customer added successfully.")

        elif choice == '2':
            list_customers(service_provider)

        elif choice == '3':
            product_name = input("Enter product name: ")
            product_description = input("Enter product description: ")
            product_price = float(input("Enter product price: "))
            product_quantity = int(input("Enter product quantity: "))  # Get quantity
            category = input("Enter product category: ")  # Get the new category input
            product = Product(product_name, product_description, product_price, product_quantity, category)  # Updated line
            service_provider.add_product(product)
            print("Product added successfully.")

        elif choice == '4':
            customer_id = int(input("Enter customer ID: "))
            order_details = []
            total_amount = 0

            while True:
                product_id = int(input("Enter product ID to order: "))
                quantity = int(input("Enter quantity: "))
                order_detail = OrderDetail(None, product_id, quantity)  # OrderID will be set later
                order_details.append(order_detail)

                # Fetch product price to calculate total amount
                with service_provider._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT Price FROM Products WHERE ProductID = ?", (product_id,))
                    price = cursor.fetchone()
                    if price:
                        total_amount += price[0] * quantity
                    else:
                        print("Product not found.")

                more = input("Do you want to add more products? (y/n): ")
                if more.lower() != 'y':
                    break

            order = Order(customer_id, datetime.now(), total_amount)  # Include order date
            service_provider.place_order(order, order_details)
            print("Order placed successfully.")

        elif choice == '5':
            product_id = int(input("Enter product ID to update quantity: "))
            new_quantity = int(input("Enter new quantity: "))
            try:
                service_provider.update_product_quantity(product_id, new_quantity)
                print("Product quantity updated successfully.")
            except Exception as e:
                print(f"Error updating product quantity: {e}")

        elif choice == '6':
            order_id = int(input("Enter order ID to track status: "))
            try:
                order_status = service_provider.track_order_status(order_id)
                print(f"Order Status: {order_status}")
            except Exception as e:
                print(f"Error tracking order status: {e}")

        elif choice == '7':
            show_sales_report_menu(service_provider)

        elif choice == '8':
            update_customer_menu(service_provider)

        elif choice == '9':
            process_payment(service_provider)

        elif choice == '10':
            delete_product(service_provider)

        elif choice == '11':
            category = input("Enter category to search: ")
            products = service_provider.search_products_by_category(category)
            if products:
                for product in products:
                    print(f"Product ID: {product.ProductID}, Name: {product.ProductName}, Price: {product.Price}, Stock: {product.StockQuantity}")
            else:
                print("No products found in this category.")

        elif choice == '12':
            show_order_total(service_provider)  # New functionality to show order total

        elif choice == '13':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
