import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[apm]+\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    mdates = []
    for i in range(0, len(dates)):
        output = dates[i]
        strencode = output.encode("ascii", "ignore")
        strdecode = strencode.decode()
        mdates.append(strdecode)

    df = pd.DataFrame({'user_message': messages, 'message_date': mdates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M%p - ')
    df['message_date'] = df['message_date'].dt.strftime('%d/%m/%Y %H:%M')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['message_date'] = pd.to_datetime(df['message_date'])

    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['day_name'] = df['message_date'].dt.day_name()

    return df

