import pandas as pd

Data = [
     [1,"John Doe", "RockHill", "CT", "doe@gmail.com"],
     [2,"Jane Smith", "Ashburn", "VA", "Jane@gmail.com"],
     [3, "Jim Brown","Maryland Heights", "MO", "jim@example.com"],
     [4, "Alice Johnson","Reston", "VA", "alice@example.com"],
     [5, "Bob Martin", "Cincinnati","OH", "bob@example.com"],
]
Df = pd.DataFrame(Data, columns=["customer_id", "customer_name", "city", "state", "email"])
Df.to_csv("customer_data.csv", index=False)

print("Customer_data.csv created.")