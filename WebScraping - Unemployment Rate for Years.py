import requests
import json
import re

def get_bls_unemployment_rate(api_key, startyear, endyear):
    #Defined both the URL and Series ID for the BLS API
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    series_id = "LAUST060000000000003"  # Series ID
    state_codes = {'06': 'California'}  # Dictionary to map state codes to names
    state_code = re.search(r"LAUST(\d{2})\d{8}", series_id).group(1)

    #Constructs the API request payload

    payload = json.dumps({
        "seriesid": [series_id],
        "startyear": startyear,
        "endyear": endyear,
        "registrationkey": api_key
    })

    #Sends API request and receives response
    response = requests.post(url, data=payload, headers={"Content-Type": "application/json"})

    #Checks if request is successful, if so, extract data from response
    if response.status_code == 200:
        data = response.json()
        if data['status'] == "REQUEST_SUCCEEDED":
            #Extracts unemployment rate data from API response
            series_data = data['Results']['series'][0]['data']
            unemployment_data = {}
            for entry in series_data:
                #Extracts year, unemployment rate, and state name from each entry
                year = entry['year']
                value = entry['value']
                state = state_codes[state_code]  # Look up the state name from the dictionary
                #Stores unemployment rate data within a dictionary, with year as key
                unemployment_data[year] = {'unemployment rate': value, 'state': state}
            return unemployment_data
        else:
            #If request fails, return error message
            return "Failed to fetch data: " + data['message']
    else:
        #If request fails, return error message with HTTP status
        return f"Request failed with status code {response.status_code}"
#Sets API Key, start year, alongside end year for data
api_key = "e5fb40526b4b4d0eae3da1e6d2673306" 
startyear = "2020"
endyear = "2023"

#Retrieves unemployment data for California
unemployment_data = get_bls_unemployment_rate(api_key, startyear, endyear)


#If data is successfully acquired, write to the text file 'unemployment_data.txt'
if isinstance(unemployment_data, dict):
    with open("unemployment_data.txt", "w") as f:
        #Write headers for the columns
        f.write("Year\tState\t     Unemployment %\n")
        for year, data in unemployment_data.items():
            #Extract unemployment rate, state name, and year
            value = data['unemployment rate']
            state = data['state']

            #Extract the year from dictionary key using regex
            year = re.search(r"\d{4}", year).group()

            #Write the data into the file
            f.write(f"{year}\t{state}   {value}\n")
else:
    #If data wasn't successfully retrieved, the print an error message
    print(unemployment_data)


