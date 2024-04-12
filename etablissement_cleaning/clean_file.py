
# HEADER : siren,nic,siret,statutDiffusionEtablissement,dateCreationEtablissement,trancheEffectifsEtablissement,anneeEffectifsEtablissement,activitePrincipaleRegistreMetiersEtablissement,dateDernierTraitementEtablissement,etablissementSiege,etatAdministratifUniteLegale,statutDiffusionUniteLegale,unitePurgeeUniteLegale,dateCreationUniteLegale,categorieJuridiqueUniteLegale,denominationUniteLegale,sigleUniteLegale,denominationUsuelle1UniteLegale,denominationUsuelle2UniteLegale,denominationUsuelle3UniteLegale,sexeUniteLegale,nomUniteLegale,nomUsageUniteLegale,prenom1UniteLegale,prenom2UniteLegale,prenom3UniteLegale,prenom4UniteLegale,prenomUsuelUniteLegale,pseudonymeUniteLegale,activitePrincipaleUniteLegale,nomenclatureActivitePrincipaleUniteLegale,identifiantAssociationUniteLegale,economieSocialeSolidaireUniteLegale,societeMissionUniteLegale,caractereEmployeurUniteLegale,trancheEffectifsUniteLegale,anneeEffectifsUniteLegale,nicSiegeUniteLegale,dateDernierTraitementUniteLegale,categorieEntreprise,anneeCategorieEntreprise,complementAdresseEtablissement,numeroVoieEtablissement,indiceRepetitionEtablissement,dernierNumeroVoieEtablissement,indiceRepetitionDernierNumeroVoieEtablissement,typeVoieEtablissement,libelleVoieEtablissement,codePostalEtablissement,libelleCommuneEtablissement,libelleCommuneEtrangerEtablissement,distributionSpecialeEtablissement,codeCommuneEtablissement,codeCedexEtablissement,libelleCedexEtablissement,codePaysEtrangerEtablissement,libellePaysEtrangerEtablissement,identifiantAdresseEtablissement,coordonneeLambertAbscisseEtablissement,coordonneeLambertOrdonneeEtablissement,complementAdresse2Etablissement,numeroVoie2Etablissement,indiceRepetition2Etablissement,typeVoie2Etablissement,libelleVoie2Etablissement,codePostal2Etablissement,libelleCommune2Etablissement,libelleCommuneEtranger2Etablissement,distributionSpeciale2Etablissement,codeCommune2Etablissement,codeCedex2Etablissement,libelleCedex2Etablissement,codePaysEtranger2Etablissement,libellePaysEtranger2Etablissement,etatAdministratifEtablissement,enseigne1Etablissement,enseigne2Etablissement,enseigne3Etablissement,denominationUsuelleEtablissement,activitePrincipaleEtablissement,nomenclatureActivitePrincipaleEtablissement,caractereEmployeurEtablissement,geoloc

# We want to keep :
# - siren
# - dateCreationEtablissement
# - denominationUniteLegale
# - coordonneeLambertAbscisseEtablissement
# - coordonneeLambertOrdonneeEtablissement

splited_lines = []
newLines = []
i = 0
with open('C:/Users/Alexa/Documents/Projects/Alessia/Seine-Saint-Denis_ScreenCityDataEngineering/etablissement_cleaning/etablissements_geoloc.csv', 'r', encoding="utf8") as f:
    lines = f.readlines()
    header = lines[0].split(',')
    example = lines[5].split(',')
    j = 0
    for headerName in header:
        print(j, ":", headerName, example[j])
        j += 1

    for line in lines[1:]:
        
        data = line.split(',')
        if len(data) > 83:
            continue
        splited_lines.append(data)

    splited_lines.sort(key=lambda x: x[4])

    for data in splited_lines: 
        i += 1


        geoloc = data[82].replace('\n', '')
        X = geoloc.split(';')[15]
        Y = geoloc.split(';')[16]
        newLines.append({
            "siren": data[0],
            "dateCreationEtablissement": data[4],
            "denominationUniteLegale": data[15],
            "X": X,
            "Y": Y,
            "IS_ONE_PERSON" : data[14] == "1000" # categorie juridique unité legal is Entrepreneur indiciuel  == 1000
        })
        if i % 1000 == 0:
            print(f'{i/len(lines) * 100} %')

with open('C:/Users/Alexa/Documents/Projects/Alessia/Seine-Saint-Denis_ScreenCityDataEngineering/etablissement_cleaning/etablissements_geoloc_cleaned.csv', 'w', encoding='utf8') as f:

    f.write('siren,dateCreationEtablissement,denominationUniteLegale,isOnePerson,X,Y\n')

    for line in newLines:
        f.write(f"{line['siren']},{line['dateCreationEtablissement']},{line['denominationUniteLegale']},{line['IS_ONE_PERSON']},{line['X']},{line['Y']}\n")

print('Done')
