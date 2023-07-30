import pandas as pd 
import sqlite3 as sql
from datetime import datetime, timedelta

conn = sql.connect('amazon-analytics.db')

### Sales Day Aggregates 

query = '''
WITH customer_aggs AS 
    (
        SELECT 
            AccountId AS Customer
            , SUBSTR(Marketplace, 10) AS Marketplace
            , ReportDate AS Date
            , COUNT(DISTINCT(ProductId)) AS "Active Products"
            , SUM(Orders) AS "Number of Orders"
            , SUM(Quantity) AS "Items Sold"
            , SUM(Sales) AS "Sales"
            , AVG(Sales / Quantity) AS "Average Price"

        FROM sales 
        GROUP BY 1, 2, 3
    ) 
    
SELECT 
    *
FROM customer_aggs 
'''

sales_dt_df = pd.read_sql(query, conn).groupby(['Marketplace', 'Date']).agg(['sum', 'mean', 'median']).reset_index()

sales_dt_df.columns = sales_dt_df.columns.to_flat_index()
cols = sales_dt_df.columns

for col in cols:
    if col[1] == 'sum':
        sales_dt_df = sales_dt_df.rename(columns= {col: '{} {}'.format('Total', col[0])})
    if col[1] == 'mean':
        sales_dt_df = sales_dt_df.rename(columns= {col: '{} {}'.format('Average', col[0])})
    if col[1] == 'median':
        sales_dt_df = sales_dt_df.rename(columns= {col: '{} {}'.format(col[1].capitalize(), col[0])})
    else: 
        sales_dt_df = sales_dt_df.rename(columns= {col: '{}'.format(col[0])})

sales_dt_df['Date'] = pd.to_datetime(sales_dt_df['Date'])

### Sales Period Aggregates

query = '''
WITH customer_day_aggs AS 
    (
        SELECT 
            AccountId AS Customer 
            , SUBSTR(Marketplace, 10) AS Marketplace 
            , ReportDate AS Date 
            , SUM(Orders) AS Orders 
            , SUM(Quantity) AS Quantity 
            , SUM(Sales) AS Sales 
        FROM sales 
        GROUP BY 1, 2, 3 
    )
, customer_aggs AS 
    (
        SELECT 
            Customer
            , Marketplace
            , CASE 
                WHEN Date IN ('2020-10-13', '2020-10-14') THEN 'Prime Day'
                ELSE 'Non-Prime Day'
            END AS Period 
            , AVG(Orders) * 2 AS "2-Day Orders" 
            , AVG(Quantity) * 2 AS "2-Day Quantity" 
            , AVG(Sales) * 2 AS "2-Day Sales" 
        FROM customer_day_aggs 
        GROUP BY 1, 2, 3
        HAVING 
            COUNT(DISTINCT(Date)) > 1
    )
    
SELECT 
    *
FROM customer_aggs 
'''

df = pd.read_sql(query, conn).groupby(['Marketplace', 'Period']).agg(['mean', 'median']).reset_index()

df.columns = df.columns.to_flat_index()
cols = df.columns

for col in cols:
    if col[1] == 'mean':
        df = df.rename(columns= {col: '{} {}'.format('Average', col[0])})
    if col[1] == 'median':
        df = df.rename(columns= {col: '{} {}'.format(col[1].capitalize(), col[0])})
    else: 
        df = df.rename(columns= {col: '{}'.format(col[0])})
        
sales_df = df
del df 

### Ads Period Aggregates

query = ''' 
WITH prep AS 
    (
        SELECT 
            AccountId AS Customer
            , SUBSTR(Marketplace, 10) AS Marketplace 
            , SUBSTR(SponsoredType, 10) AS "Sponsored Type"
            , SUBSTR(ReportDate, LENGTH(ReportDate) - 3) || '-' ||
                SUBSTR('0' || SUBSTR(ReportDate, 1, INSTR(ReportDate, '/') - 1), -2) || '-' ||
                SUBSTR('0' || SUBSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), 1, INSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), '/') - 1), -2)
                AS Date
            , COALESCE(Impressions, 0) AS Impressions 
            , COALESCE(Clicks, 0) AS Clicks
            , COALESCE(Costs, 0) AS Costs 
            , COALESCE(Sales, 0) AS Sales
            , COALESCE(UnitsSold, 0) AS Quantity
        FROM ads 
        WHERE 
            Costs > 0
    )
, customer_aggs AS 
    (
        SELECT 
            Customer
            , Marketplace
            , "Sponsored Type"
            , CASE 
                WHEN Date IN ('2020-10-13', '2020-10-14') THEN 'Prime Day'
                ELSE 'Non-Prime Day'
            END AS Period 
            , AVG(Impressions) * 2 AS "2-Day Impressions" 
            , AVG(Clicks) * 2 AS "2-Day Clicks" 
            , SUM(Clicks) / SUM(Impressions) * 100 AS CTR
            , AVG(Costs) * 2 AS "2-Day Ad Spending" 
            , SUM(Costs) / SUM(Clicks) AS CPC
            , AVG(Sales) * 2 AS "2-Day Ad Revenue" 
            , SUM(Costs) / SUM(Sales) * 100 AS ACoS 
            , SUM(Sales) / SUM(Costs) * 100 AS ROAS 
        FROM prep 
        GROUP BY 1, 2, 3, 4 
        HAVING 
            COUNT(DISTINCT(Date)) > 1
    )

SELECT 
    *
FROM customer_aggs
'''

df1 = pd.read_sql(query, conn).groupby(['Marketplace', 'Sponsored Type', 'Period']).agg(['mean', 'median']).reset_index()

df1.columns = df1.columns.to_flat_index()
cols = df1.columns

for col in cols:
    if col[1] == 'mean':
        df1 = df1.rename(columns= {col: '{} {}'.format('Average', col[0])})
    if col[1] == 'median':
        df1 = df1.rename(columns= {col: '{} {}'.format(col[1].capitalize(), col[0])})
    else: 
        df1 = df1.rename(columns= {col: '{}'.format(col[0])})
        
query = ''' 
WITH prep AS 
    (
        SELECT 
            AccountId AS Customer
            , SUBSTR(Marketplace, 10) AS Marketplace 
            , SUBSTR(ReportDate, LENGTH(ReportDate) - 3) || '-' ||
                SUBSTR('0' || SUBSTR(ReportDate, 1, INSTR(ReportDate, '/') - 1), -2) || '-' ||
                SUBSTR('0' || SUBSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), 1, INSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), '/') - 1), -2)
                AS Date
            , COALESCE(Impressions, 0) AS Impressions 
            , COALESCE(Clicks, 0) AS Clicks
            , COALESCE(Costs, 0) AS Costs 
            , COALESCE(Sales, 0) AS Sales
            , COALESCE(UnitsSold, 0) AS Quantity
        FROM ads 
        WHERE 
            Costs > 0
    )
, customer_aggs AS 
    (
        SELECT 
            Customer
            , Marketplace
            , CASE 
                WHEN Date IN ('2020-10-13', '2020-10-14') THEN 'Prime Day'
                ELSE 'Non-Prime Day'
            END AS Period 
            , AVG(Impressions) * 2 AS "2-Day Impressions" 
            , AVG(Clicks) * 2 AS "2-Day Clicks" 
            , SUM(Clicks) / SUM(Impressions) * 100 AS CTR
            , AVG(Costs) * 2 AS "2-Day Ad Spending" 
            , SUM(Costs) / SUM(Clicks) AS CPC
            , AVG(Sales) * 2 AS "2-Day Ad Revenue" 
            , SUM(Costs) / SUM(Sales) * 100 AS ACoS 
            , SUM(Sales) / SUM(Costs) * 100 AS ROAS 
        FROM prep 
        GROUP BY 1, 2, 3
        HAVING 
            COUNT(DISTINCT(Date)) > 1
    )

SELECT 
    *
FROM customer_aggs
'''

df2 = pd.read_sql(query, conn).groupby(['Marketplace', 'Period']).agg(['mean', 'median']).reset_index()

df2.columns = df2.columns.to_flat_index()
cols = df2.columns

for col in cols:
    if col[1] == 'mean':
        df2 = df2.rename(columns= {col: '{} {}'.format('Average', col[0])})
    if col[1] == 'median':
        df2 = df2.rename(columns= {col: '{} {}'.format(col[1].capitalize(), col[0])})
    else: 
        df2 = df2.rename(columns= {col: '{}'.format(col[0])})

df2['Sponsored Type'] = 'All'
df2 = df2[df1.columns]

ads_df = df1.append(df2).sort_values(['Marketplace', 'Sponsored Type', 'Period'])
del df1
del df2 

query = '''
WITH prep AS -- referenced in measuring median price 
    (
        SELECT 
            *
            , Sales / Quantity AS Price
            , ROW_NUMBER() OVER (PARTITION BY AccountId, Marketplace, ReportDate ORDER BY (Sales / Quantity)) AS rn 
            , COUNT(*) OVER (PARTITION BY AccountId, Marketplace, ReportDate) AS counter
        FROM sales 
    )

SELECT 
    AccountId AS Customer
    , SUBSTR(Marketplace, 10) AS Marketplace
    , ReportDate AS Date
    , COUNT(DISTINCT(ProductId)) AS "Active Products"
    , SUM(Orders) AS "Number of Orders"
    , SUM(Quantity) AS "Items Sold"
    , SUM(Sales) AS "Sales"
    , AVG(Sales / Quantity) AS "Average Price"
    , AVG
        (
             CASE counter % 2 -- Check odd or even
                WHEN 0 THEN CASE WHEN rn IN (counter / 2, counter / 2 + 1) THEN Price END -- When even then two middle values are not null
                WHEN 1 THEN CASE WHEN rn = counter / 2 + 1 THEN Price END -- When odd then middle value is not null
             END
        ) AS "Median Price"
FROM prep 
GROUP BY 1, 2, 3
'''

sales_customer_aggs = pd.read_sql(query, conn)
sales_customer_aggs['Date'] = pd.to_datetime(sales_customer_aggs['Date'])

query = ''' 
WITH prep AS 
    (
        SELECT 
            AccountId AS Customer
            , SUBSTR(Marketplace, 10) AS Marketplace 
            , SUBSTR(SponsoredType, 10) AS "Sponsored Type"
            , SUBSTR(ReportDate, LENGTH(ReportDate) - 3) || '-' ||
                SUBSTR('0' || SUBSTR(ReportDate, 1, INSTR(ReportDate, '/') - 1), -2) || '-' ||
                SUBSTR('0' || SUBSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), 1, INSTR(SUBSTR(ReportDate, INSTR(ReportDate, '/') + 1), '/') - 1), -2)
                AS Date
            , COALESCE(Impressions, 0) AS Impressions 
            , COALESCE(Clicks, 0) AS Clicks
            , CASE 
                WHEN COALESCE(Clicks, 0) = 0 AND COALESCE(Impressions, 0) = 0 THEN 0
                ELSE (COALESCE(Clicks, 0) / COALESCE(Impressions, 0)) * 100
            END AS CTR 
            , COALESCE(Costs, 0) AS "Ad Costs" 
            , COALESCE(Sales, 0) AS "Ad Revenue"
            , COALESCE(Costs, 0) / COALESCE(Clicks, 0) AS CPC
            , CASE 
                WHEN COALESCE(Costs, 0) = 0 AND COALESCE(Sales, 0) != 0 THEN 0
                ELSE (COALESCE(Costs, 0) / COALESCE(Sales, 0)) * 100
            END AS ACoS 
            , (COALESCE(Sales, 0) / COALESCE(Costs, 0)) * 100 AS ROAS 
            , COALESCE(UnitsSold, 0) AS Quantity
        FROM ads 
    ) 

SELECT 
    Customer 
    , Marketplace 
    , 'All' AS "Sponsored Type"
    , Date 
    , SUM(Impressions) AS Impressions 
    , SUM(Clicks) AS Clicks 
    , CASE 
        WHEN SUM(Clicks) = 0 AND SUM(Impressions) = 0 THEN 0
        ELSE (SUM(Clicks) / SUM(Impressions)) * 100
    END AS CTR 
    , SUM("Ad Costs") AS "Ad Costs" 
    , SUM("Ad Revenue") AS "Ad Revenue" 
    , SUM("Ad Costs") / SUM(Clicks) AS CPC
    , CASE 
        WHEN SUM("Ad Costs") = 0 AND SUM("Ad Revenue") != 0 THEN 0
        ELSE (SUM("Ad Costs") / SUM("Ad Revenue")) * 100
    END AS ACoS 
    , (SUM("Ad Revenue") / SUM("Ad Costs")) * 100 AS ROAS 
    , SUM(Quantity) AS Quantity 
FROM prep 
GROUP BY 
    Customer 
    , Marketplace
    , Date

UNION 

SELECT 
    *
FROM prep
'''

ads_customer_aggs = pd.read_sql(query, conn)
ads_customer_aggs['Date'] = pd.to_datetime(ads_customer_aggs['Date'])