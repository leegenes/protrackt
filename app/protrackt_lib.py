from datetime import datetime

def convert_to_date(date_string):
    if not date_string or isinstance(date_string, datetime):
        return date_string

    return datetime.strptime(date_string, '%Y-%m-%d')

def write_requested_attributes(db_object, request_content):
    for key in request_content.keys():
            if hasattr(db_object, key):
                setattr(db_object, key, request_content[key])
    return True

if __name__ == "__main__":
    pass
