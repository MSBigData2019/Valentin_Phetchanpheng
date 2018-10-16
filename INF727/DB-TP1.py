
# coding: utf-8

# # TP1 - Finding Keys using Functional Dependencies 
# --------------------------
# 
# In this lab, we are going to learn 
# 
# - how to use Jupyter
# - how to use SQLite
# - how to discover keys in relations
# 
# ## How to use Jupyter
# 
# To execute a cell, click on it, and then use SHIFT+ENTER (this will execute the contents of the cell, and move down to the next one!)
# 
# To edit a cell, click on it. If the cell uses markdown code, then use ENTER to edit it.
# 
# See the Help menu for other useful keyboard commands. You can always use the menu bar instead as well.
# 

# In[1]:


print("Hello world!")


# Another example:

# In[2]:


for i in range(1,10):
    print(i)


# #### Exercise 1
# 
# Print numbers 1 to 9 in reverse order

# In[3]:


# Méthode 1 
for i in range (1,10):
    print(10 - i)
    
print('\n')
    
# Méthode 2 
for i in reversed(range(1,10)):
    print(i)


# ## How to use SQLite
# 
# To work with SQL easily in a notebook, we'll load the ipython-sql extension as follows:

# In[4]:


get_ipython().run_line_magic('load_ext', 'sql')
get_ipython().run_line_magic('sql', 'sqlite://')


# We are going to create a table:

# In[5]:


get_ipython().run_cell_magic('sql', 'DROP TABLE IF EXISTS T;', "CREATE TABLE T(course VARCHAR, classroom INT, time INT);\nINSERT INTO T VALUES ('CS 364', 132, 900);\nINSERT INTO T VALUES ('CS 245', 140, 1000);\nINSERT INTO T VALUES ('EE 101', 210, 900);")


# Let's run our first SQL query:

# In[6]:


get_ipython().run_line_magic('sql', 'SELECT * FROM T;')


# #### Exercise 2
# 
# List the name of the courses with time less than 950

# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT course FROM T WHERE time < 950;')


# ## How to discover keys in relations
# 
# Now, we are going to work with functional dependencies, keys and closures. Our final goal is going to build a method to find keys in a relation.
# 
# ### Functional Dependencies
# 
# Recall that given a set of attributes  $\{A_1, \dots, A_n\}$ and a set of FDs $\Gamma$
# 
# The closure, denoted $\{A_1, \dots, A_n\}^+$, is defined to be the largest set of attributes B s.t. $$A_1,\dots,A_n \rightarrow B \text{ using } \Gamma.$$
# 
# We're going to use some functions to compute the closure of a set of attributes and other such operations (_from CS145 Stanford_)

# In[8]:


# Source code

def to_set(x):
  """Convert input int, string, list, tuple, set -> set"""
  if type(x) == set:
    return x
  elif type(x) in [list, set]:
    return set(x)
  elif type(x) in [str, int]:
    return set([x])
  else:
    raise Exception("Unrecognized type.")

def fd_to_str(lr_tuple):
    lhs = lr_tuple[0]
    rhs = lr_tuple[1]
    return ",".join(to_set(lhs)) + " -> " + ",".join(to_set(rhs))

def fds_to_str(fds): return "\n\t".join(map(fd_to_str, fds))

def set_to_str(x): return "{" + ",".join(x) + "}"

def fd_applies_to(fd, x): 
  lhs, rhs = map(to_set, fd)
  return lhs.issubset(x)

def print_setup(A, fds):
  print("Attributes = " + set_to_str(A))
  print("FDs = \t" + fds_to_str(fds))

def print_fds(fds):
  print("FDs = \t" + fds_to_str(fds))    


# Now, let's look at a concrete example. For example, the code for
# 
# attributes = { name, category, color, department, price}
# 
# and functional dependencies:
# 
# name $\rightarrow$ color
# 
# category $\rightarrow$ department
# 
# color, category $\rightarrow$ price
# 
# is the following:

# In[9]:


attributes  = set(["name", "category", "color", "department", "price"]) # These are the attribute set.
fds = [(set(["name"]),"color"),
         (set(["category"]), "department"),
         (set(["color", "category"]), "price")]

print_setup(attributes, fds)


# ### Closure of a set of Attributes
# 
# Let's implement the algorithm for obtaining the closure of a set of attributes:

# In[10]:


def compute_closure(x, fds, verbose=False):
    bChanged = True        # We will repeat until there are no changes.
    x_ret    = x.copy()    # Make a copy of the input to hold x^{+}
    while bChanged:
        bChanged = False   # Must change on each iteration
        for fd in fds:     # loop through all the FDs.
            (lhs, rhs) = map(to_set, fd) # recall: lhs -> rhs
            if fd_applies_to(fd, x_ret) and not rhs.issubset(x_ret):
                x_ret = x_ret.union(rhs)
                if verbose:
                    print("Using FD " + fd_to_str(fd))
                    print("\t Updated x to " + set_to_str(x_ret))
                bChanged = True
    return x_ret


# As an example, let's compute the closure for the attribute "name":

# In[11]:


A = set(["name"])
compute_closure(A,fds, True)


# #### Exercise 3
# 
# Is the attribute "name" a superkey for this relation? Why?

# Non car le closure de name est {'color', 'name'} ce qui ne permet pas de déterminer les autres attributs

# ### Keys and Superkeys
# 
# Next, we'll add some new functions now for finding superkeys and keys.  Recall:
# * A _superkey_ for a relation $R(B_1,\dots,B_m)$ is a set of attributes $\{A_1,\dots,A_n\}$ s.t.
# $$ \{A_1,\dots,A_n\} \rightarrow B_{j} \text{ for all } j=1,\dots m$$
# * A _key_ is a minimal (setwise) _superkey_
# 
# The algorithm to determine if a set of attributes $A$ is a superkey for $X$ is actually very simple (check if $A^+=X$):

# In[12]:


def is_superkey_for(A, X, fds, verbose=False): 
    return X.issubset(compute_closure(A, fds, verbose=verbose))


# Is "name" a superkey of the relation?

# In[13]:


is_superkey_for(A, attributes, fds)


# Then, to check if $A$ is a key for $X$, we just confirm that:
# * (a) it is a superkey
# * (b) there are no smaller superkeys (_Note that we only need to check for superkeys of one size smaller_)

# In[14]:


import itertools
def is_key_for(A, X, fds, verbose=False):
    subsets = set(itertools.combinations(A, len(A)-1))
    return is_superkey_for(A, X, fds) and         all([not is_superkey_for(set(SA), X, fds) for SA in subsets])


# Now, let's look at another example:
# 
# attributes = { cru, type, client, remise}
# 
# and functional dependencies:
# 
# cru $\rightarrow$ type
# 
# type, client $\rightarrow$ remise
# 
# #### Exercise 4
# 
# Is "cru" and "client" a key of the relation? Why?

# In[15]:


attributes_test  = set(["cru", "type", "client", "remise"]) # These are the attribute set.
fds_test = [(set(["cru"]),"type"),
         (set(["type", "client"]), "remise")]

print_setup(attributes_test, fds_test)


# In[16]:


# Compute closure
A1 = set(["cru", "client"])
compute_closure(A1,fds_test, True)


# In[17]:


is_key_for(A1, attributes_test, fds_test)


# Because it's a superkey and it is minimal. 

# ### Closure of a set of functional dependencies
# 
# The algorithm to find the closure of a set of functional dependencies is the following:

# In[18]:


import itertools
def findsubsets(S,m):
    return set(itertools.combinations(S, m))
def closure(X, fds, verbose=False):
    c = []
    for size in range(1, len(X)):
        subsets = findsubsets(X, size) 
        for SA in subsets:      # loop through all the subsets.
            cl = compute_closure(set(SA), fds, verbose)
            if len(cl.difference(SA)) > 0: 
                c.extend([(set(SA), cl.difference(SA))])
    return c


# Let's see some examples of how to use it:

# In[19]:


attributes1 = set(['A', 'B', 'C', 'D'])
fds1 = [(set(['A', 'B']), 'C'),
     (set(['A', 'D']), 'B'),
     (set(['B']), 'D')]
print_fds(closure(attributes1, fds1))


# In[20]:


attributes2 = set (['CRU', 'TYPE', 'CLIENT', 'REMISE'])
fds2 = [(set(['CRU']), 'TYPE'),
     (set(['TYPE', 'CLIENT']), 'REMISE')]
print_fds(closure(attributes2, fds2))


# In[21]:


attributes3 = set( ['N VEH', 'TYPE', 'COULEUR', 'MARQUE', 'PUISSANCE'])
fds3 = [(set(['N VEH']), 'TYPE'), 
      (set(['N VEH']), 'COULEUR'),
      (set(['TYPE']), 'MARQUE'),
      (set(['TYPE']), 'PUISSANCE')]
print_fds(closure(attributes3,fds3))


# Now, let's write a method to find superkeys of the relations:
# 

# In[22]:


def superkeys(X, fds, verbose=False):
    c = []
    for size in range(1, len(X)):
        subsets = findsubsets(X, size)
        for SA in subsets:
            cl = compute_closure(set(SA), fds, verbose)
            if cl == X and len(cl.difference(SA)) > 0: ## cl = X
                c.extend([SA])
    return c


# In[23]:


superkeys(attributes1, fds1)


# Let's see some examples:

# In[24]:


superkeys(attributes2, fds2)


# In[25]:


superkeys(attributes3, fds3)


# #### Exercise 5
# 
# Implement a `keys` method to find keys of a relation.
# 
# **Note**: If there exist multiple keys of a relation, the `keys` method should return at least one of them.

# In[61]:


def keys(X, fds, verbose=False):
    super_key = to_set(superkeys(X, fds))
    for el in super_key:
        if is_key_for(set(el), X, fds) == True:
            print(el)


# In[62]:


attributes1 = set(['A', 'B', 'C', 'D'])
fds1 = [(set(['A', 'B']), 'C'),
     (set(['A', 'D']), 'B'),
     (set(['B']), 'D')]

test = set(["C","A", "B"])
is_key_for(test, attributes1, fds1)


# Test it 

# In[63]:


keys(attributes1, fds1)


# In[64]:


keys(attributes2, fds2)


# In[65]:


keys(attributes3, fds3)

