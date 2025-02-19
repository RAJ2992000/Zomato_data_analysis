import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Database connection credentials
DB_USER = "root"
DB_PASSWORD = "Rajkumarn123"
DB_HOST = "localhost"
DB_NAME = "zomato"

# Create database engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Function to execute SELECT queries
@st.cache_data
def execute_query(query, params=None):
    """Executes a SQL SELECT query and returns a DataFrame."""
    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, connection, params=params)
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

# Function to execute INSERT, UPDATE, DELETE queries
def execute_modify_query(query, params=None):
    """Executes INSERT, UPDATE, DELETE queries."""
    try:
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(query), params or {})
        st.success("Query executed successfully!")
    except Exception as e:
        st.error(f"Query execution failed: {e}")

# Streamlit page configuration
st.set_page_config(page_title="Zomato Analytics", layout="wide")
st.title("📊 Zomato Data Analytics Dashboard")

# Sidebar selection menu
st.sidebar.header("📌 Source")
option = st.sidebar.radio("Select an Option", ["SQL Queries", "CRUD Operations"])

# 1️⃣ **SQL Queries Section**
if option == "SQL Queries":
    st.sidebar.subheader("📌 Select Query")
    
    queries = {
        "List all customers' names and emails.": '''
      SELECT name, email FROM customers_table;
    ''',
    "List all premium customers' names and emails.": '''
        SELECT name, email FROM customers_table WHERE is_premium = 1;
    ''',
    "Customers per Location": """
        SELECT location, COUNT(*) AS total_customers 
        FROM customers_table 
        GROUP BY location 
        ORDER BY total_customers DESC;
    """,
    "Top 5 Customers by Orders": """
        SELECT name, total_orders 
        FROM customers_table 
        ORDER BY total_orders DESC 
        LIMIT 5;
    """,
    "Customers with Rating > 4": """
        SELECT name, average_rating 
        FROM customers_table 
        WHERE average_rating > 4;
    """,
    "Customer Details with Total Orders & Preferred Cuisine": """
        SELECT c.name, c.email, c.phone, c.preferred_cuisine, c.total_orders
        FROM customers_table c;
    """,
    "Orders with Customer & Restaurant Details": """
        SELECT o.order_id, c.name AS customer_name, r.name AS restaurant_name, o.total_amount, o.order_status
        FROM manages_order o
        JOIN customers_table c ON o.customer_id = c.customer_id
        JOIN manages_restaurant_infos r ON o.restaurant_id = r.restaurant_id;
    """,
    "Total Revenue per Restaurant": """
        SELECT r.name AS restaurant_name, SUM(o.total_amount) AS total_revenue
        FROM manages_order o
        JOIN manages_restaurant_infos r ON o.restaurant_id = r.restaurant_id
        GROUP BY r.name
        ORDER BY total_revenue DESC;
    """,
    "Top 5 Customers with Highest Orders": """
        SELECT c.name AS cus_name, COUNT(o.order_id) AS total_orders
        FROM customers_table c
        JOIN manages_order o ON c.customer_id = o.customer_id
        GROUP BY c.name
        ORDER BY total_orders DESC
        LIMIT 5;
    """,
    "Restaurants with Avg Rating >= 4 & Orders > 500": """
        SELECT name, rating, total_orders
        FROM manages_restaurant_infos
        WHERE rating >= 4 AND total_orders > 500;
    """,
    "Most Common Payment Method": """
        SELECT payment_mode, COUNT(*) AS total_usage
        FROM manages_order
        GROUP BY payment_mode
        ORDER BY total_usage DESC
        LIMIT 1;
    """,
    "Total Revenue per Payment Mode": """
        SELECT payment_mode, SUM(total_amount) AS total_revenue
        FROM manages_order
        GROUP BY payment_mode
        ORDER BY total_revenue DESC;
    """,
    "Orders with Discount > 10": """
        SELECT * FROM manages_order WHERE discount_applied > 10;
    """,
    "Total Deliveries per Delivery Person": """
        SELECT dp.name, COUNT(d.delivery_id) AS total_deliveries
        FROM delivery_table_data d
        JOIN delivery_person_table dp ON d.delivery_person_id = dp.delivery_person_id
        GROUP BY dp.name
        ORDER BY total_deliveries DESC;
    """,
    "Average Delivery Time per Restaurant": """
        SELECT r.name AS restaurant_name, AVG(d.delivery_time) AS avg_delivery_time
        FROM delivery_table_data d
        JOIN manages_order o ON d.order_id = o.order_id
        JOIN manages_restaurant_infos r ON o.restaurant_id = r.restaurant_id
        GROUP BY r.name
        ORDER BY avg_delivery_time ASC;
    """,
    "Top Delivery Persons (Deliveries > 100 & Rating > 4.5)": """
        SELECT name, total_deliveries, average_rating
        FROM delivery_person_table
        WHERE total_deliveries > 100 AND average_rating > 4.5;
    """,
    "Orders Taking Longer than Estimated Time": """
        SELECT d.order_id, d.delivery_time, d.estimated_time, d.delivery_status
        FROM delivery_table_data d
        WHERE d.delivery_time > d.estimated_time;
    """,
    "Total Orders per Restaurant": """
        SELECT r.name AS restaurant_name, COUNT(o.order_id) AS total_orders
        FROM manages_order o
        JOIN manages_restaurant_infos r ON o.restaurant_id = r.restaurant_id
        GROUP BY r.name
        ORDER BY total_orders DESC;
    """,
    "Restaurants with No Orders": """
        SELECT r.name
        FROM manages_restaurant_infos r
        LEFT JOIN manages_order o ON r.restaurant_id = o.restaurant_id
        WHERE o.order_id IS NULL;
    """,
    "Most Common Vehicle Type for Deliveries": """
        SELECT vehicle_type, COUNT(*) AS usage_count
        FROM delivery_table_data
        GROUP BY vehicle_type
        ORDER BY usage_count DESC
        LIMIT 1;
    """

    }

    selected_query = st.sidebar.selectbox("Choose a Query", list(queries.keys()))

    if st.sidebar.button("Run Query"):
        query = queries[selected_query]
        df = execute_query(query)
        st.session_state.df = df  # Store results in session state

    if 'df' in st.session_state and not st.session_state.df.empty:
        st.subheader(f"🔍 Results for: **{selected_query}**")
        st.dataframe(st.session_state.df)

        # Check if the DataFrame has integer/numeric columns for charting
        numeric_columns = st.session_state.df.select_dtypes(include=['int64', 'float64']).columns

        if len(numeric_columns) > 0:
            st.subheader("📊 Chart Representation")

            # Automatically choose the first string column as X-axis
            non_numeric_columns = st.session_state.df.select_dtypes(include=['object']).columns
            if len(non_numeric_columns) > 0:
                x_axis = non_numeric_columns[0]
                y_axis = numeric_columns[0]

                fig = px.bar(st.session_state.df, x=x_axis, y=y_axis, title=f"{y_axis} per {x_axis}")
                st.plotly_chart(fig)
            else:
                st.warning("No categorical column found for visualization.")
        else:
            st.info("No numerical data available for charting.")

# 2️⃣ **CRUD Operations Section**
elif option == "CRUD Operations":
    st.subheader("🚀 CRUD Operations")

    crud_option = st.radio("Select CRUD Operation", ["Create", "Read", "Update", "Delete"])

    # **Create (Insert) Operation**
    if crud_option == "Create":
        st.subheader("📝 Insert New Order")

        customer_name = st.text_input("Customer Name")
        email = st.text_input("Email")
        total_orders = st.number_input("Total Orders", min_value=1)
        total_amount = st.number_input("Total Amount", min_value=0.0)
        order_status = st.selectbox("Order Status", ["Pending", "Delivered", "Cancelled"])

        if st.button("Insert Data"):
            query = """
                INSERT INTO manages_order (customer_name, email, total_orders, total_amount, order_status)
                VALUES (:customer_name, :email, :total_orders, :total_amount, :order_status)
            """
            params = {
                'customer_name': customer_name,
                'email': email,
                'total_orders': total_orders,
                'total_amount': total_amount,
                'order_status': order_status
            }
            execute_modify_query(query, params)

    # **Read (View) Operation**
    elif crud_option == "Read":
        st.subheader("📖 View Orders")

        if st.button("View All Orders"):
            query = "SELECT * FROM manages_order"
            df = execute_query(query)
            st.dataframe(df)

    # **Update Operation**
    elif crud_option == "Update":
        st.subheader("🔄 Update Order")

        order_id = st.number_input("Enter Order ID to Update", min_value=1)
        new_order_status = st.selectbox("New Order Status", ["Pending", "Delivered", "Cancelled"])

        if st.button("Update Order"):
            query = """
                UPDATE manages_order
                SET order_status = :new_order_status
                WHERE order_id = :order_id
            """
            params = {'new_order_status': new_order_status, 'order_id': order_id}
            execute_modify_query(query, params)

    # **Delete Operation**
    elif crud_option == "Delete":
        st.subheader("🗑️ Delete Order")

        order_id_to_delete = st.number_input("Enter Order ID to Delete", min_value=1)

        if st.button("Delete Order"):
            query = "DELETE FROM manages_order WHERE order_id = :order_id_to_delete"
            params = {'order_id_to_delete': order_id_to_delete}
            execute_modify_query(query, params)
