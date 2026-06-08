import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns


df = pd.read_csv('data.csv')


#Data cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
# print(df.columns)
df.drop_duplicates()

df['area']=df['area'].astype(str).str.replace(",","").astype(int)
df['rate_per_sqft']=df['rate_per_sqft'].astype(str).str.replace(",","").astype(int)
df['price']=df['price'].astype(str).str.replace(",","").astype(float)


df['status']=df['status'].str.strip().str.lower()
df['rera_approval']=df['rera_approval'].str.strip().str.lower().map({'approved by rera':True, 'not approved by rera': False})
df['flat_type']=df['flat_type'].str.strip().str.lower()

df.drop_duplicates()
# print(df.info())


#Which is the costliest flat in the dataset?
costliest_flat = df.loc[df['price'].idxmax()]
print(f"The costliest flat in the dataset is {costliest_flat['bhk_count']} BHK flat located in {costliest_flat['locality']} with a price of {costliest_flat['price']}")


#Which locality has the highest average price?
avg_price_by_locality = df.groupby('locality')['price'].mean().sort_values(ascending=False)
print("The locality with the highest average price is", avg_price_by_locality.index[0])


# Which locality has the highest rate per square foot?
highest_rate_per_sqft = df.groupby('locality')['rate_per_sqft'].mean().sort_values(ascending=False)
print(f"The locality with the highest average rate per square foot is {highest_rate_per_sqft.index[0]}")


#Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price= df[df['status'] == 'under construction']['price'].mean()
if ready_to_move_avg_price > under_construction_avg_price:
    print("Ready to move properties cost more than under construction properties.")
else:
    print("Under construction properties cost more than ready to move properties.")    


# Do RERA-approved properties command a price premium?
if df[df['rera_approval'] == True]['price'].mean() > df[df['rera_approval'] == False]['price'].mean():
    print("RERA-approved properties command a price premium.")
else:
    print("RERA-approved properties do not command a price premium.")


#How does area (sqft) impact property price?
sns.scatterplot(x='area',y='price',data=df)
plt.title('Area vs Price')
plt.xlabel('Area(sqft)')
plt.ylabel('Price')
plt.show()


#Which BHK configuration is the most expensive based on per sqft rate?
avg_rate_by_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().sort_values(ascending=False)
print(f"The most expensive BHK configuration on average is {avg_rate_by_bhk.index[0]}")


#Which property type (Apartment, Floor, Plot) is the costliest?
most_expensive_property_type = df.groupby('flat_type')['price'].mean().sort_values(ascending=False)
print(f"The costliest property type on average is {most_expensive_property_type.index[0]}")


#Do certain builders or companies consistently price higher?And print name of top 5 companies.
top_5_companies = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending = False).head()
print(f"The top 5 companies that consistently price higher are: {top_5_companies}") 


#Are larger homes always more expensive per square foot?
sns.scatterplot(x='area', y='rate_per_sqft',data=df)
plt.title('Area vs Rate per sqft')
plt.xlabel('Area(sqft)')
plt.ylabel('Rate per sqft')
plt.show()
