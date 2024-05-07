#!/usr/bin/env python
# coding: utf-8

# # Retail Case Study - (abhay.gupt018@gmail.com)

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import datetime


# In[ ]:





# In[2]:


customer = pd.read_csv('Customer.csv')
product = pd.read_csv('prod_cat_info.csv')
transaction = pd.read_csv('Transactions.csv')


# In[3]:


customer.shape


# In[4]:


product.shape


# In[5]:


transaction.shape


# In[6]:


customer.head(5)


# In[7]:


product.head(5)


# In[8]:


transaction.head(5)


# # Q1.

# In[9]:


product.rename(columns={'prod_sub_cat_code':'prod_subcat_code'}, inplace=True)


# In[ ]:





# In[10]:


temp_table = pd.merge(left=transaction, right=customer, left_on='cust_id', right_on='customer_Id', how='left')
temp_table


# In[11]:


customer_final = pd.merge(left =temp_table , right = product, left_on= ['prod_subcat_code','prod_cat_code'], right_on=['prod_subcat_code','prod_cat_code'], how='left')
customer_final


# In[12]:


customer_final.dtypes


# In[13]:


customer_final['tran_date'] = pd.to_datetime(customer_final['tran_date'], format = '%d-%m-%Y', errors = 'coerce')
customer_final['tran_date']


# In[14]:


customer_final['DOB'] = pd.to_datetime(customer_final['DOB'],format = '%d-%m-%Y')
customer_final['DOB']


# In[ ]:





# # Q2.

# In[15]:


# a.

customer_final.columns


# In[16]:


customer_final.dtypes


# In[17]:


#b.

customer_final.head(10)


# In[18]:


customer_final.tail(10)


# In[19]:


#c.
customer_final.describe()


# In[20]:


#d.

customer_final.loc[:,customer_final.dtypes=='object'].describe()


# # Q3.

# In[21]:


# Histogram


# In[22]:


conti_customer = customer_final.loc[:,['prod_subcat_code','prod_cat_code', 'Qty', 'Rate', 'Tax', 'total_amt']]


# In[23]:


conti_customer.columns


# In[24]:


for var in conti_customer.columns:
    conti_customer[var].plot(kind='hist')
    plt.title(var)
    plt.show()


# In[25]:


# Bar Chart


# In[26]:


category_customer = customer_final.loc[:,customer_final.dtypes=='object']


# In[27]:


category_customer.head()


# In[28]:


plt.figure(figsize=(5, 5))
sns.countplot(data=category_customer, x='Gender')
plt.show()


# In[29]:


plt.figure(figsize=(4,4))
sns.countplot(data=category_customer, x ='Store_type')
plt.show()


# In[30]:


plt.figure(figsize=(6,7))
category_customer.groupby('prod_subcat')['prod_subcat'].count().plot(kind='barh')
plt.xlabel('Count')
plt.ylabel('Product Subcategory')
plt.show()


# # Q4.

# In[31]:


#a.
customer_final.sort_values(by='tran_date')


# In[32]:


earliest_date = customer_final.tran_date.min()
latest_date = customer_final.tran_date.max()

time_period = (latest_date - earliest_date).days
print(f"The time period of the available transaction data is from {earliest_date} to {latest_date}.")
print(f"The total duration of the transaction data is: {time_period}")


# In[33]:


#b.
negative_transaction = customer_final.loc[customer_final.total_amt < 0 ,'transaction_id'].count()
print('Count of transaction where the total amount of transaction is negative', negative_transaction)


# # Q5.

# In[34]:


customer_final.head(1)


# In[35]:


popular_product = customer_final.groupby(['Gender', 'prod_cat'])[['Qty']].sum().reset_index()


# In[36]:


popular_product


# In[37]:


popular_product.pivot(index='Gender', columns='prod_cat', values='Qty')


# # Products that are popular among males are:
# 
# * Books
# * Clothing
# * Electronics
# * Home and kitchen
# 
# 
# # Products that are popular among females are:
# 
# * Bags
# * Footwear

# In[ ]:





# # Q6. 

# In[38]:


customer_final.head(1)


# In[39]:


popular_products = customer_final.groupby('city_code')['customer_Id'].count().sort_values(ascending=False)


# In[40]:


popular_products


# In[41]:


percentage_of_customers = round((popular_products[4.0]/popular_products.sum())*100,2)


# In[42]:


percentage_of_customers


# In[43]:


print("City code 4.0 has the maximum customers and the percentage of customers from that city is ",percentage_of_customers)


# # Q7.

# In[44]:


customer_final.groupby('Store_type')[['Qty','Rate']].sum().sort_values(by='Qty', ascending = False)


# In[45]:


print('e-Shop store sell the maximum products by value and by quantity')


# # Q8. 

# In[46]:


customer_final.head(1)


# In[47]:


amount_earned = customer_final.pivot_table(index='prod_cat', columns='Store_type', values='total_amt', aggfunc='sum')


# In[48]:


round(amount_earned,2)


# In[49]:


amount_earned.loc[['Electronics', 'Clothing'],['Flagship store']].sum()


# # Q9

# In[50]:


amount_earned_male = customer_final.pivot_table(index='prod_cat', columns='Gender', values='total_amt', aggfunc='sum')


# In[51]:


round(amount_earned_male,2)


# In[52]:


temp =amount_earned_male.loc['Electronics','M']


# In[53]:


print('Total amount earned by male of Electronics category is', temp)


# # Q10

# In[54]:


# creating a new dataframe with positive value only

positive_tran = customer_final.loc[customer_final['total_amt']>0,:]


# In[55]:


positive_tran


# In[56]:


# creating a newdata frame for unique transaction

uni_trans = positive_tran.groupby(['customer_Id','prod_cat','prod_subcat'])['transaction_id'].count().reset_index()


# In[57]:


uni_trans


# In[58]:


# now finding the customers which have unique transactions greater than 10
uni_trans_count = uni_trans.groupby('customer_Id')['transaction_id'].count().reset_index()


# In[59]:


uni_trans_count.head()


# In[60]:


uni_trans_count[uni_trans_count['transaction_id']>10]


# In[61]:


print('No Customers have more than 10 unique transaction.')


# # Q11
11.(a)
# In[62]:


customer_final['Age'] = (datetime.datetime.today().year - customer_final['DOB'].dt.year)
filtered_customer_final = customer_final[(customer_final['Age'] >= 25) & (customer_final['Age'] <= 35) & (customer_final['prod_cat'].isin(['Electronics', 'Books']))]
total_amount_spent = filtered_customer_final['total_amt'].sum()
print("Total amount spent on Electronics and Books by customers aged between 25 and 35:", total_amount_spent)

11(b)
# In[63]:


temp = filtered_customer_final[(filtered_customer_final['tran_date'] >= '2014-01-01') & (filtered_customer_final['tran_date'] <= '2014-03-01')]
total_amount_spent = temp['total_amt'].sum()
print("Total amount spent by customers aged between 25 and 35 between 1st Jan, 2014 and 1st Mar, 2014:", total_amount_spent)


# In[ ]:




