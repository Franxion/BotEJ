from datetime import datetime, timedelta

# Function to generate a list of valid dates
def generate_dates(start_date, num_days):
    # Parse the start_date string to a datetime object
    start = datetime.strptime(start_date, "%Y-%m-%d")
    # Generate a list of dates
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]
    return dates

# # Example usage
# start_date = "2025-02-25"  # Starting date
# num_days = 10  # Number of dates to generate
# date_list = generate_dates(start_date, num_days)
#
# print(date_list)
