import matplotlib.pyplot as plt
import datetime


def timestamp_graph(monthly_data):
    months = sorted(monthly_data.keys())
    print(months)
    positive_counts = [monthly_data[month]['Positive'] for month in months]
    negative_counts = [monthly_data[month]['Negative'] for month in months]
    total_counts = [monthly_data[month]['total'] for month in months]
    # months = [datetime.datetime(year, month, 1) for year, month in monthly_data]

    # Plotting positive comment counts
    plt.figure(figsize=(10, 6))
    plt.plot(months, positive_counts, marker='o',color='green', label='Positive')
    plt.plot(months, negative_counts, marker='o', color='red', label='Negative')
    plt.title('Positive Comment Counts Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plotting negative comment counts
    # plt.figure(figsize=(10, 6))
    # plt.plot(months, negative_counts, marker='o', color='red', label='Negative')
    # plt.title('Negative Comment Counts Over Time')
    # plt.xlabel('Month')
    # plt.ylabel('Number of Comments')
    # plt.xticks(rotation=45)
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

    # Plotting total comment counts
    plt.figure(figsize=(10, 6))
    plt.plot(months, total_counts, marker='o', color='orange', label='Total')
    plt.title('Total Comment Counts Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
    
def Pie_chart(data):
    colors = ['green', 'red', 'gray']
    explode = (0.1, 0, 0)
    plt.figure(figsize=(8, 6))
    plt.pie(data.values(), explode=explode, labels=data.keys(), colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Comments', fontsize=16, fontweight='bold')
    plt.gca().set_aspect('equal')   # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.rcParams['font.size'] = 12  # Increase label font size
    plt.rcParams['font.weight'] = 'normal'  # Reset font weight to normal for labels

    # Show the plot
    plt.show()
    


def engagement_graph(monthly_data):

    months = sorted(monthly_data.keys())
    total_counts = [monthly_data[month]['total'] for month in months]
    months = [datetime.datetime(year, month, 1) for year, month in monthly_data]
    sorted_data = sorted(zip(months, total_counts), key=lambda x: x[1], reverse=True)
    sorted_months, sorted_counts = zip(*sorted_data)
    sorted_months = sorted_months[:10]
    sorted_counts = sorted_counts[:10]
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(sorted_months)), sorted_counts, color='skyblue')
    plt.yticks(range(len(sorted_months)), [month.strftime('%B %Y') for month in sorted_months])  # Use full month name
    plt.xlabel('Number of Comments')
    plt.ylabel('Month')
    plt.title('Comment Counts Over Time')
    plt.gca().invert_yaxis()  # Invert y-axis to display months from top to bottom
    plt.tight_layout()
    plt.show()
    
    
def engage_graph(monthly_data):
    print(monthly_data)
    months = list(monthly_data.keys())
    total_counts = list(monthly_data.values())

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(months)), total_counts, color='skyblue')
    plt.xticks(range(len(months)), months, rotation=45)  # Display months on x-axis with rotation
    plt.ylabel('Number of Comments')
    plt.xlabel('Month')
    plt.title('Comment Counts Over Time')
    plt.tight_layout()
    plt.show()