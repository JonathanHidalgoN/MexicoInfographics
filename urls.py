# This file contains the urls for the API requests, and a boolean value to indicate if the request is a time series or not.
urls = {
    "population": (
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041,6200027788,5000000002,1002000001/es/0700/true/BISE/2.0/[Aquí va tu Token]?type=json",
        False,
    ),
    "male_female_population": (
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041,6200027788,5000000002,1002000002,1002000003/es/0700/false/BISE/2.0/[Aquí va tu Token]?type=json",
        True,
    ),
    "0-4/10-14/15-19/20-24/male_female_population": (
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041,6200027788,5000000002,1002000059,1002000060/es/0700/false/BISE/2.0/[Aquí va tu Token]?type=json",
        True,
    ),
    "25-29/30-34/35-39/40-44/male_female_population": (
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041,6200027788,5000000002,1002000074,1002000075,1002000077,1002000078,1002000080,1002000081,1002000083/es/0700/false/BISE/2.0/[Aquí va tu Token]?type=json",
        True,
    ),
    "5-9/50_54/55-59/male_female_population": (
        "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041,6200027788,5000000002,1002000089,1002000090,1002000092,1002000093,1002000095,1002000096/es/0700/false/BISE/2.0/[Aquí va tu Token]?type=json",
        True,
    ),
}
