# Zomato Data Analytics and Management Tool

## Project Overview
This project aims to enhance operational efficiency and improve customer satisfaction by analyzing food delivery data. The primary objective is to build an interactive Streamlit tool that enables seamless data entry and management for orders, customers, restaurants, and deliveries. The tool also supports robust database operations like adding columns or creating new tables dynamically while maintaining compatibility with existing code.

## Business Use Cases
- **Order Management:** Identifying peak ordering times and locations, tracking delayed and canceled deliveries.
- **Customer Analytics:** Analyzing customer preferences and order patterns, identifying top customers based on order frequency and value.
- **Delivery Optimization:** Analyzing delivery times and delays to improve logistics, tracking delivery personnel performance.
- **Restaurant Insights:** Evaluating the most popular restaurants and cuisines, monitoring order values and frequency by restaurant.

## Approach
### 1) Dataset Creation
- Use Python (Faker) to generate synthetic datasets for customers, orders, restaurants, and deliveries.
- Populate the SQL database with these datasets.

### 2) Database Design
- Create normalized SQL tables for Customers, Orders, Restaurants, and Deliveries.
- Ensure compatibility for dynamic schema changes (e.g., adding columns, creating new tables).

### 3) Data Entry Tool
- Develop a Streamlit app for:
  - Adding, updating, and deleting records in the SQL database.
  - Dynamically creating new tables or modifying existing ones.

### 4) Data Insights
- Use SQL queries and Python to extract insights like peak times, delayed deliveries, and customer trends.
- Visualize the insights in the Streamlit app.

### 5) OOP Implementation
- Encapsulate database operations in Python classes.
- Implement robust and reusable methods for CRUD (Create, Read, Update, Delete) operations.

### 6) Order Management
- Identifying peak ordering times and locations.
- Tracking delayed and canceled deliveries.

### 7) Customer Analytics
- Analyzing customer preferences and order patterns.
- Identifying top customers based on order frequency and value.

### 8) Delivery Optimization
- Analyzing delivery times and delays to improve logistics.
- Tracking delivery personnel performance.

### 9) Restaurant Insights
- Evaluating the most popular restaurants and cuisines.
- Monitoring order values and frequency by restaurant.

## Results
By the end of this project, the following deliverables will be achieved:
- A fully functional SQL database for managing food delivery data.
- An interactive Streamlit app for data entry and analysis.
- Dynamic compatibility with database schema changes.
- Comprehensive insights into order trends, delivery performance, and customer behavior.
- 
## Technologies Used
- **SQL** - Database design and queries.
- **Python** - Data processing and analysis.
- **Streamlit** - Interactive web-based data entry and visualization.
- **Data Engineering** - Managing and processing structured data.
- **Object-Oriented Programming (OOP)** - Modular and reusable code.
- **Relational Databases** - Efficient data storage and retrieval.

## Dataset
- **Source:** Synthetic dataset generated using Python.
- **Format:** CSV or direct insertion into SQL tables.
- **Library:** Faker Python to create dummy dataset.


