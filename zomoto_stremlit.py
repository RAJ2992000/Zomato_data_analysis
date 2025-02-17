import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DB_USER = "root"
DB_PASSWORD = "Rajkumarn123"
DB_HOST = "localhost"
DB_NAME = "zomato"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

@st.cache_data
def execute_query(query):
    """Executes the given SQL query and returns a DataFrame."""
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

st.set_page_config(page_title="Zomato Analytics", layout="wide")
st.title("📊 Zomato Data Analytics Dashboard")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f7f7f7;
            padding: 10px;
        }
        [data-testid="stSidebar"] h2 {
            color: #d62728;
        }
        [data-testid="stSidebar"] select {
            background-color: #f0f0f0;
            color: #333;
            font-weight: bold;
        }
        [data-testid="stSidebar"] button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("📌 Select Query")

# Dictionary of Queries
queries = {
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

# Sidebar dropdown for query selection
selected_query = st.sidebar.selectbox("Choose a Query", list(queries.keys()))

# Execute and display selected query
if st.sidebar.button("Run Query"):
    query = queries[selected_query]
    df = execute_query(query)
    if not df.empty:
        if "total_customers" in df.columns or "total_revenue" in df.columns:
            st.bar_chart(df.set_index(df.columns[0]))  # Bar chart for numerical data
        st.dataframe(df)
    else:
        st.warning("No data found.")

# Reset Button
if st.sidebar.button("🔄 Reset"):
    st.rerun()
