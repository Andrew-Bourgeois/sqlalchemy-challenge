# sqlalchemy-challenge
UNC-CH-DA - Module 10 Challenge - sqlalchemy-challenge

### **INSTRUCTIONS**
* Clone the repository to your local machine
* cd into the "sqlalchemy-challenge/SurfsUp/" directory.
* 

### **BACKGROUND**

You have decided treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with trip planning, we will do some climate analysis for the area.

### **REQUIREMENTS**

## **Jupyter Notebook Database Connection (10 Points)**
* Use the SQLALchemy 'create_engine()' function to connect to your SQLite database (1 point)

* Use the SQLAlchemy 'automap_base()' function to reflect your table into classes(3 points)

* Save references to the classes named 'station' and 'measurement' (4 points)

* Link Python to the database by creating a SQLAlchemy session (1 point)

* Close your session at the end of your notebook (1 point)

## **Precipitation Analysis (16 points)**
* Create a query that finds the most recent date in the dataset (8/23/2017) (2 points)

* Create a query that collects only the 'date' and 'precipitation' for the last year of data without passing the date as a varaible (4 points)

* Save the query results to a Pandas DataFrame to create 'date' and 'precipitation' columns (2 points)

* Sort the DataFrame by 'date' (2 points)

* Plot the results by using the DataFrame 'plot' method with 'date' as the x and 'precipitation' as the y variables (4 points)

* Use Pandas to print the sumamry statistics for the precipitation data (2 points)

## **Station Analysis (16 points)**
* Design a query that correctly finds the number of stations in the dataset (9) (2 points)

* Design a query that correctly lists the stations and observation counts in descending order and finds the most active station (USC00519281) (2 points)

* Design a query that correctly finds the min, max, and average temperatures for the most active station (USC00519281) (3 points)

* Design a query to get the previous 12 months of temperature observation (TOBS) data that filters by the station that has the greatest number of observations (3 points)

* Save the query results to a Pandas DataFrame (2 points)

* Correctly plot a histogram with bins=12 for the last year of data using tobs as the column to count. (4 points)

## **API Static Routes (15 points)**
A **precipitation route** that:
*   Returns json with the date as the key and the value as the precipitation (3 points)
*   Only returns the jsonified percipitation data for the last year in the database (3 points)

A **stations route** that:
*   Returns the jsonified data of all the stations in the database (3 points)

A **tobs route** that:
*   Returns jsonified data for the most active station (USC00519281) (3 points)
*   Only returns the jsonified data for the last year of data (3 points)

## **API Dynamic Route (15 points)**
A **start route** that:
*   Accepts the start date as a parameter from the url (2 points)
*   Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset (4 points)

A **start/end route** that:
*   Accepts the start and end dates as parameters from the URL (3 points)
*   Returns the min, max, and average temperatures calculated from the given start date to the given end date (6 points)

## **Coding Conventions and Formatting (8 points)**
* Place imports at the top of the file, just after any module comments and docstrings, and before module globals and constants. (2 points)

* Name functions and variables with lowercase characters, with words separated by underscores. (2 points)

* Follow DRY (Don't Repeat Yourself) principles, creating maintainable and reusable code. (2 points)

* Use concise logic and creative engineering where possible. (2 points)

## **Deployment and Submission (6 points)**
* Submit a link to a GitHub repository that’s cloned to your local machine and contains your files. (2 points)

* Use the command line to add your files to the repository. (2 points)

* Include appropriate commit messages in your files. (2 points)

## **Comments (4 points)**
* Be well commented with concise, relevant notes that other developers can understand. (4 points)


### **RESOURCES**
* Starter Files: https://static.bc-edx.com/data/dl-1-2/m10/lms/starter/Starter_Code.zip 
* Sorting SQLAlchemy results in descending order: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending 