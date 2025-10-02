import pandas as pd
import os 
import sqlite3 

orders_df = pd.read_csv("sample_data.csv")
customers_df= pd.read_csv("customer_data.csv")
claim_df = pd.read_csv ("Medicare_Hospital_Spending_by_Claim.csv")

print("orders data: ")
print(orders_df.head())

print("\nCustomers Data: ")
print(customers_df.head())

print("\n Claim Data")
print(claim_df.head())

connection = sqlite3.connect("app.db")

orders_df.to_sql("orders", connection, if_exists = "replace", index = False)
customers_df.to_sql("customer", connection, if_exists = "replace", index= False)
claim_df.to_sql("claim", connection, if_exists = "replace", index = False)


connection.close()
print("\n Database Created Successfully: app.db")