import csv



def monthly(date_dict):
    monthly_data = {}
    for date, counts in date_dict.items():
        month = (date.year, date.month)
        if month not in monthly_data:
            monthly_data[month] = {'positive': 0, 'negative': 0, 'total': 0}
        monthly_data[month]['positive'] += counts['positive']
        monthly_data[month]['negative'] += counts['negative']
        monthly_data[month]['total'] += counts['total']
        
    # print(monthly_data)
    return monthly_data

        
def csv_file(comments_dict):
    for name in comments_dict.keys():
        filename = f"comment/{name}.csv"
        headers = ['S.No.', 'Comment']

        # Write the comments to a CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the header row
            writer.writerow(headers)
            
            # Write each comment along with its serial number
            for i, comment in enumerate(comments_dict[name], start=1):
                writer.writerow([i, comment])
