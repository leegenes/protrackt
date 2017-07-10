from datetime import datetime

def convert_to_date(date_string):
    if not date_string:
        return date_string

    return datetime.strptime(date_string, '%Y-%m-%d')

if __name__ == "__main__":
    pass
