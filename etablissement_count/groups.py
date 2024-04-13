
# HEADER : siren,dateCreationEtablissement,denominationUniteLegale,isOnePerson,X,Y


lines_without_count = []
counts = {} # counts by denominationUniteLegale

i = 0
with open('C:/Users/Alexa/Documents/Projects/Alessia/Seine-Saint-Denis_ScreenCityDataEngineering/etablissement_count/etablissements_geoloc_cleaned.csv', 'r', encoding="utf8") as f:
    f.readline() # skip header
    lines_without_count = f.readlines()
    
for line in lines_without_count:
    data = line.replace('\n','').split(',')
    if data[2] not in counts:
        counts[data[2]] = 1
    counts[data[2]] += 1

with open('C:/Users/Alexa/Documents/Projects/Alessia/Seine-Saint-Denis_ScreenCityDataEngineering/etablissement_count/etablissements_geoloc_cleaned_with_count.csv', 'w', encoding='utf8') as f:
    f.write('siren,dateCreationEtablissement,denominationUniteLegale,isOnePerson,X,Y,appearances\n')
    for line in lines_without_count:
        data = line.split(',')
        name = data[2]
        if(data[3] == "True"):
            count = 1
        else:
            count = counts[name]

        orig_line = (','.join(data)).replace('\n','')
        f.write(f"{orig_line},{count}\n")
