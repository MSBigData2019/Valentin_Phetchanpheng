
# coding: utf-8

# # TP2 - DB Normalization and Querying
# 
# The objectives of this TP are:
# 1. Apply normalization 1NF -> 2NF -> 3NF
# 2. Perform SQL queries on the normalized database
# 
# In this TP, we will use a database **`wine.db`** (available in the course's website) containing wine information related to 'production' and 'sales'. 
# 
# > Production <---> Wine <---> Sales
# 
# 
# ---
# 
# ### Working with db files in Jupyter
# - Python provides an interface for SQLite through the *sqlite3* module
# - The **`%%sql`** magic builds upon it (and other tools) to enable the usage of SQL commands within a Jupyter Notebook as in common SQL clients.
# - Before proceeding, make sure that **`wine.db`** is in the same path as this notebook.
#   - If **`wine.db`** is not in the same path, an empty **`wine.db`** file will be created, resulting in errors in later steps of the TP.
# - The SQLite module in Python commits transactions automatically, this means that any change in the DB is immediately written to the file, e.g. creating/deleting tables.
#   -  For this reason, it is recommended to have a backup of **`wine.db`** as it is provided in the course's website.
# 
# ---

# **`wine.db`** contains the following unnormalized tables:
# 
# <center>**Master1**</center>
# 
# |*Attribute*|         *Description*          |
# | -------   |--------------------------------|
# | NV        | Wine number                    |
# | CRU       | Vineyard or group of vineyards |
# | DEGRE     | Alcohol content                |
# | MILL      | Vintage year                   |
# | QTE       | Number of bottles harvested    |
# | NP        | Producer number                |
# | NOM       | Producer's last name           |
# | PRENOM    | Producer's first name          |
# | REGION    | Production region              |
# 
# From wikipedia:
# 
# __Cru__: Often used to indicate a specifically named and legally defined vineyard or ensemble of vineyards and the vines "which grow on [such] a reputed terroir; by extension of good quality." The term is also used to refer to the wine produced from such vines.
# 
# 
# <center>**Master2**</center>
# 
# |*Attribute*|                         *Description*                  |
# | -------   |--------------------------------------------------------|
# | NV        | Wine number                                            |
# | CRU       | Vineyard or group of vineyards                         |
# | DEGRE     | Alcohol content                                        |
# | MILL      | Vintage year                                           |
# | DATES     | Buying date                                            |
# | LIEU      | Place where the wine was sold                          |
# | QTE       | Number of bottles bought                               |
# | NB        | Client (buveur) number                                 |
# | NOM       | Client's last name                                     |
# | PRENOM    | Client's first name                                    |
# | TYPE      | Type of client by volume of purchases                  |
# | REGION    | Administrative Region (different to production region) |
# 

# In[36]:


import sqlite3    # Python interface for SQLite databases


# In[37]:


def printSchema(connection):
    # Function to print the DB schema
    # Source: http://stackoverflow.com/a/35092773/4765776
    for (tableName,) in connection.execute(
        """
        select NAME from SQLITE_MASTER where TYPE='table' order by NAME;
        """
    ):
        print("{}:".format(tableName))
        for (
            columnID, columnName, columnType,
            columnNotNull, columnDefault, columnPK,
        ) in connection.execute("pragma table_info('{}');".format(tableName)):
            print("  {id}: {name}({type}){null}{default}{pk}".format(
                id=columnID,
                name=columnName,
                type=columnType,
                null=" not null" if columnNotNull else "",
                default=" [{}]".format(columnDefault) if columnDefault else "",
                pk=" *{}".format(columnPK) if columnPK else "",
            ))


# In[38]:


conn = sqlite3.connect('wine.db')
c = conn.cursor()
print("Database schema:")
printSchema(conn)           # An usefull way to viualize the content of the database


# From this point we will use __%%sql__ magic

# In[39]:


get_ipython().run_line_magic('load_ext', 'sql')
get_ipython().run_line_magic('sql', 'sqlite:///wine.db')


# # PART I: Database normalization

# The first task on this TP is the normalization of the wine data. In its current state both tables **Master1** and **Master2** are in the First Normal Form (1NF).
# 
# By inspecting the content of these tables we can see that multiple tuples have NULL values.

# In[40]:


get_ipython().run_cell_magic('sql', 'SELECT *', 'FROM Master1\nLIMIT 10;')


# * Notice that Jupyter *displays* 'None' instead of 'NULL'. 
#   - This is only to comply with python notation.
# * To account for NULL values, your SQL queries must test explicitly for 'NULL'.
# 
# Another problem in **Master1** and **Master2** is data redundancy, for example:

# In[41]:


get_ipython().run_cell_magic('sql', 'SELECT *', 'FROM Master1\nWHERE NP = 5 ; ')


# ---
# 
# Additional resource for Normalization:
# 
# https://www.youtube.com/watch?v=UrYLYV7WSHM
# 
# ---

# In[42]:


get_ipython().run_cell_magic('sql', 'SELECT *', "FROM Master2\nWHERE NV = '32';")


# #### Exercise 1.1
# 
# Convert table **Master1** to the Second Normal Form (2NF) or Third Normal Form (3NF) as applicable.
# * Explain your answer
# * List main functional dependencies (not all of them)
# * Describe the schema of new tables and how they relate
#   * You can write Tables as above or you can insert images in the notebook.
#   
# Remember that **`wine.db`** contains information related to wine 'production' and 'sells'.
# 
# > Production <---> Wine <---> Sales
# 
# A good start point is to look for the 'Wine' attributes.
# 
# **Hint:** Look for redundant information between the master tables.
2NF pour Master 1 :
R(NV, CRU, MILL, DEGRE)  key = NV
R(NP, NOM, PRENOM, REGION)  key = NP
R(NV, NP, QTE)   key = NV, NP
# #### Exercise 1.2
# 
# Convert table **Master2** to the Second Normal Form (2NF) or Third Normal Form (3NF) as applicable.
# * Explain your answer
# * List main functional dependencies (not all of them)
# * Describe the schema of new tables and how they relate
#   * You can write Tables as above or you can insert images in the notebook.
# 
# **Note:** For this part, consider that a wine can be bought in multiple locations and multiple times per day.
2NF pour Master 2 :
R(NV, CRU, MILL, DEGRE)   key = NV
R(NB, NOM, PRENOM, TYPE)	  key = NP (Client)
R(NV, NB, DATES, QTE, LIEU, REGION)    key = NP, NB, DATES
# Once you have defined the 2NF or 3NF (as applicable) we need to split the data into new tables.
# 
# A table can be created from the result of a query.
# 
# In the following example we will create a new table "dummy" to store the different values of alcohol content.

# In[43]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS dummy;', '\n-- Create dummy table\nCREATE TABLE dummy AS\nSELECT DISTINCT DEGRE\nFROM MASTER1;')


# In[44]:


print("\nContent of the database")
printSchema(conn)


# In[45]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM dummy;')


# Looking into "dummy", we notice that our query includes NULL. This is not allowed if we were to use DEGRE as key for a table.
# 
# To correct this, we need to change the query to explicitly test for NULL as follows:

# In[46]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS dummy;', '\n-- Create dummy table\nCREATE TABLE dummy AS\nSELECT DISTINCT DEGRE\nFROM MASTER1\nWHERE DEGRE IS NOT NULL;\n\nSELECT *\nFROM dummy;')


# Notice that we use `NULL` given that `None` is only used for display.

# In[47]:


# Remove "dummy" table
get_ipython().run_line_magic('sql', 'DROP TABLE IF EXISTS dummy;')


# #### Exercise 1.3
# 
# Create the new tables from Master1:

# In[48]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS Vin;', '\n-- Create Vin table\nCREATE TABLE Vin AS\nSELECT DISTINCT NV, CRU, MILL, DEGRE\nFROM MASTER1\nWHERE NV IS NOT NULL;\n\nSELECT * FROM Vin LIMIT 10;')


# In[49]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS Producteur;', '\n-- Create Producteur table\nCREATE TABLE Producteur AS\nSELECT DISTINCT NP, NOM, PRENOM, REGION\nFROM MASTER1\nWHERE NP IS NOT NULL;\n\nSELECT * FROM Producteur LIMIT 10;')


# In[50]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS Recolte;', '\n-- Create Recolte table\nCREATE TABLE Recolte AS\nSELECT DISTINCT NV, NP, QTE\nFROM MASTER1\nWHERE NV AND NP NOT NULL;\n\nSELECT * FROM Recolte LIMIT 10;')


# #### Exercise 1.4
# 
# Create the new tables from Master2:

# In[51]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS Buveur;', '\n-- Create Buveur table\nCREATE TABLE Buveur AS\nSELECT DISTINCT NB, NOM, PRENOM, TYPE, REGION\nFROM MASTER2\nWHERE NB IS NOT NULL;\n\nSELECT * FROM Buveur LIMIT 10;')


# In[52]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS Achat;', '\n-- Create Achat table\nCREATE TABLE Achat AS\nSELECT DISTINCT NV, NB, QTE, LIEU, DATES\nFROM MASTER2\nWHERE NV IS NOT NULL AND NB IS NOT NULL;\n\nSELECT * FROM Achat LIMIT 10;')


# # PART II: SQL QUERIES
# 
# In the second part of this TP you will create SQL queries to retrieve information from the database.
# 
# **Important:**
# 
# - You MUST use the normalized tables created in previous steps.
#   - The normalized tables will also be used in TP3.
# - Do NOT use **Master1** and **Master2** in your queries.

# #### Exercise 2.1
# 
# What are the different types of clients (buveurs) by volume of purchases?

# In[53]:


get_ipython().run_cell_magic('sql', '', "SELECT DISTINCT TYPE AS 'Type_of_buveurs' FROM Buveur;")


# #### Exercise 2.2
# 
# What regions produce Pommard or Brouilly?

# In[57]:


get_ipython().run_cell_magic('sql', '', 'SELECT v.CRU, p.REGION FROM Producteur p \nINNER JOIN Recolte r ON p.NP = r.NP\nINNER JOIN Vin v ON r.NV = v.NV\nWHERE v.CRU IN ("Pommard", "Brouilly")')


# #### Exercise 2.3
# 
# What regions produce Pommard and Brouilly?

# In[62]:


get_ipython().run_cell_magic('sql', '', 'SELECT p.REGION FROM Producteur p \nINNER JOIN Recolte r ON p.NP = r.NP\nINNER JOIN Vin v ON r.NV = v.NV\nWHERE v.CRU IN ("Pommard", "Brouilly")\nGROUP BY p.REGION HAVING COUNT(*) > 1 ')


# #### Exercise 2.4
# 
# Get the number of wines bught by CRU and Millésime

# In[69]:


get_ipython().run_cell_magic('sql', '', 'SELECT v.CRU, v.MILL, SUM(a.QTE) as Number_of_wines_bought FROM Vin v\nINNER JOIN Achat a ON v.NV = a.NV\nGROUP BY v.CRU, v.MILL;')


# #### Exercise 2.5
# 
# Retrieve the wine number (NV) of wines produced by more than three producers

# In[77]:


get_ipython().run_cell_magic('sql', '', 'SELECT NV, COUNT(NP) AS Number_of_producers FROM Recolte\nGROUP BY NV HAVING Number_of_producers > 3;')


# #### Exercise 2.6
# 
# Which producers have not produced any wine?

# In[94]:


get_ipython().run_cell_magic('sql', '', 'SELECT NP, NOM, PRENOM FROM Producteur\nWHERE NP NOT IN (SELECT NP FROM Recolte);')


# #### Exercise 2.7
# 
# What clients (buveurs) have bought at least one wine from 1980?

# In[23]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT a.NB, b.NOM, b.PRENOM FROM Achat a\nINNER JOIN Vin v ON a.NV = v.NV\nINNER JOIN Buveur b ON a.NB = b.NB\nWHERE v.MILL >= 1980\nORDER BY a.NB;')


# #### Exercise 2.8
# 
# What clients (buveurs) have NOT bought any wine from 1980?

# In[119]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT NB, NOM, PRENOM FROM Buveur\nWHERE NB NOT IN (SELECT DISTINCT a.NB FROM Achat a INNER JOIN Vin v ON a.NV = v.NV WHERE v.MILL = 1980)\nORDER BY NB;')


# In[123]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT a.NB, b.NOM, b.PRENOM, v.MILL FROM Achat a\nINNER JOIN Vin v ON a.NV = v.NV\nINNER JOIN Buveur b ON a.NB = b.NB\nORDER BY a.NB;')


# #### Exercise 2.9
# 
# What clients (buveurs) have bought ONLY wines from 1980?

# In[27]:


get_ipython().run_cell_magic('sql', '', 'SELECT b.NOM, b.PRENOM, SUM(a.QTE) AS bottles_bought_1980 FROM Buveur b\nINNER JOIN Achat a on b.NB = a.NB\nINNER JOIN Vin v on a.NV = v.NV\nGROUP BY b.NOM, b.PRENOM;\nEXCEPT\nSELECT b.NOM, b.PRENOM, SUM(a.QTE) AS bottles_bought_1980 FROM Buveur b\nINNER JOIN Achat a on b.NB = a.NB\nINNER JOIN Vin v on b.NV = v.NV\nWHERE v.MILL!=1980\nGROUP BY b.NOM, b.PRENOM;')


# #### Exercise 2.10
# 
# List all wines from 1980

# In[124]:


get_ipython().run_cell_magic('sql', '', 'SELECT * FROM Vin \nWHERE MILL = 1980\nORDER BY NV;')


# #### Exercise 2.11
# 
# What are the wines from 1980 bought by NB=2?

# In[139]:


get_ipython().run_cell_magic('sql', '', 'SELECT DISTINCT a.NV, v.CRU, v.MILL, v.DEGRE FROM Achat a\nINNER JOIN Vin v ON a.NV = v.NV\nWHERE v.MILL = 1980 AND NB = 2;')


# #### Exercise 2.12
# 
# What clients (buveurs) have bought ALL the wines from 1980?

# In[152]:


get_ipython().run_cell_magic('sql', '', 'SELECT NB, NOM, PRENOM FROM\n(SELECT DISTINCT a.NB, b.NOM, b.PRENOM, COUNT(v.CRU), v.MILL, v.DEGRE FROM Achat a\nINNER JOIN Vin v ON a.NV = v.NV\nINNER JOIN Buveur b ON a.NB = b.NB\nWHERE v.MILL = 1980\nGROUP BY a.NB HAVING COUNT(v.CRU) = 18);')

