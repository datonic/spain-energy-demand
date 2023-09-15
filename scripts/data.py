import pandas as pd
import requests

df = pd.DataFrame()

FIRST_DAY = pd.to_datetime('2014-01-01')

start_date = pd.to_datetime(FIRST_DAY)
start_date_str = start_date.strftime('%Y-%m-%d')
end_date = start_date + pd.DateOffset(days=15)
end_date_str = end_date.strftime('%Y-%m-%d')

yesterday = pd.to_datetime('today') - pd.DateOffset(days=1)

while start_date < yesterday:
    url = f'https://apidatos.ree.es/en/datos/demanda/demanda-tiempo-real?start_date={start_date_str}T00:00&end_date={end_date_str}T00:00&time_trunc=hour'
    response = requests.get(url)
    local_df = pd.json_normalize(response.json()['included'][0]['attributes']['values'])
    local_df['datetime'] = pd.to_datetime(local_df['datetime'], utc=True)
    df = pd.concat([df, local_df[["value", "datetime"]]])
    start_date = start_date + pd.DateOffset(days=15)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date = start_date + pd.DateOffset(days=15)
    end_date_str = end_date.strftime('%Y-%m-%d')

df.to_csv('../data/spain-energy-demand.csv', index=False)
