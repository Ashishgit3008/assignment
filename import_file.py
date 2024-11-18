import pandas as pd
import psycopg2
from datetime import datetime
import numpy as np


def parse_date(date):
    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%b %d, %Y']:
        try:
            return datetime.strptime(date, fmt).date()
        except ValueError:
            pass
    return None 

# Load the CSV file
df = pd.read_csv(r'/Users/ashish/geitpl/test.csv')

# Preprocessing steps
print("Preprocessing data...")
df['PurchaseDate'] = df['PurchaseDate'].apply()

# Handle missing values
df['ReviewRating'] = df['ReviewRating'].fillna(0) 
df['Age'] = df['Age'].fillna(df['Age'].mean())


connection = psycopg2.connect(
    dbname='testdatabase',
    user='ashishnew',
    password='12345',
    host='localhost',
    port='5432'
)

create_table_query = """
CREATE TABLE IF NOT EXISTS customer_reviews_new (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    PurchaseDate VARCHAR(255),  -- Store as VARCHAR initially to avoid date format issues
    ProductCategory VARCHAR(255),
    ReviewRating INT,
    ReviewText TEXT
);
"""

with connection.cursor() as cursor:
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'customer_reviews_new' is ready!")

insert_query = """
    INSERT INTO customer_reviews_new (CustomerID, Name, Age, PurchaseDate, ProductCategory, ReviewRating, ReviewText)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Upload data to the PostgreSQL database
try:
    with connection.cursor() as cursor:
        for index, row in df.iterrows():
            data = (
                row['CustomerID'],
                row['Name'],
                row['Age'],
                row['PurchaseDate'],
                row['ProductCategory'],
                row['ReviewRating'],
                row['ReviewText']
            )
            
            try:
                cursor.execute(insert_query, data)
            except Exception as e:
                print(f"Error inserting row {index + 1}: {e}")
                continue  # Skip the row if there's an error

        # Commit the changes to the database
        connection.commit()
        print("Data successfully uploaded into the 'customer_reviews_new' table!")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    connection.close()

preprocessed_csv_path = "customer_reviews_preprocessed.csv"
df.to_csv(preprocessed_csv_path, index=False)
print(f"Preprocessed data saved to '{preprocessed_csv_path}'")
