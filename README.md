# TDS_project_1
Project 1 for Tools in Data Science IITM online degree program

Q)An explanation of how you scraped the data

This data was scraped using GitHub REST API and requests library in Python (Pandas for using the dataframe functionality), in this code i also made use of pagination and delays of 1 second between requests to ensure i dont hit the rate limit for free usage. 

The fetch_users_in_city function queries GitHub’s search API for users in Hyderabad with more than 50 followers.
fetch_user_details function fetches details about each user
The fetch_user_repositories function fetches up to the 500 most recently pushed public repositories for each user.
The clean_company_name function standardizes company names by trimming whitespace, removing leading '@' symbols, and converting names to uppercase.
Finally my script uses pandas to save data into csvs

I extracted the created dataframes as csv files which i then exported as excel files for further analysis using Microsoft Excel.

Q)The most interesting and surprising fact you found after analyzing the the data

The most interesting and surprising fact i found out is the popular languages (in terms of average rating) used for the repositories, my initial assumption was that languages like Python, C or HTML would be popular however it seems like Perl, HCL and Arduino are well-liked. Of course the most popular in terms of number of repositories does go to the more well-known programming languages like JavaScript, Python and HTML.
 
Q)An actionable recommendation for developers based on your analysis

My recommendation would be to consider different methods of analysis, not just one, especially if you are comfortable with just one language/software only. I used excel mainly for this exercise beacuse it was na opportunity to expmnad my skills beyond python.
