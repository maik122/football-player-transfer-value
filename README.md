#  Transfer Value Prediction Web App

A web-based system that estimates football players' **transfer values** using performance and contract data. Built with **SQLite, HTML, JavaScript**, and Python for backend logic and data handling. Users can view predicted values, while admins can manage data and generate performance insights using graphs.

---

##  What It Does

- Import player data from a CSV file
- Store and manage player info in **SQLite3**
- Calculate a custom **transfer value** based on:
  - Weekly salary
  - Contract length
  - Games played and won
  - Bonus stats (e.g. FG1)
- Visualise stats with **graphs**
- Admin login panel
- Report data errors via UI

---

##  Transfer Value Formula

```python
transfer_value = weekly_salary * contract_duration * (games_won + fg1) / games_played_this_year
