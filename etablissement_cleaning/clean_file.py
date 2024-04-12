
# HEADER : siren,nic,siret,statutDiffusionEtablissement,dateCreationEtablissement,trancheEffectifsEtablissement,anneeEffectifsEtablissement,activitePrincipaleRegistreMetiersEtablissement,dateDernierTraitementEtablissement,etablissementSiege,etatAdministratifUniteLegale,statutDiffusionUniteLegale,unitePurgeeUniteLegale,dateCreationUniteLegale,categorieJuridiqueUniteLegale,denominationUniteLegale,sigleUniteLegale,denominationUsuelle1UniteLegale,denominationUsuelle2UniteLegale,denominationUsuelle3UniteLegale,sexeUniteLegale,nomUniteLegale,nomUsageUniteLegale,prenom1UniteLegale,prenom2UniteLegale,prenom3UniteLegale,prenom4UniteLegale,prenomUsuelUniteLegale,pseudonymeUniteLegale,activitePrincipaleUniteLegale,nomenclatureActivitePrincipaleUniteLegale,identifiantAssociationUniteLegale,economieSocialeSolidaireUniteLegale,societeMissionUniteLegale,caractereEmployeurUniteLegale,trancheEffectifsUniteLegale,anneeEffectifsUniteLegale,nicSiegeUniteLegale,dateDernierTraitementUniteLegale,categorieEntreprise,anneeCategorieEntreprise,complementAdresseEtablissement,numeroVoieEtablissement,indiceRepetitionEtablissement,dernierNumeroVoieEtablissement,indiceRepetitionDernierNumeroVoieEtablissement,typeVoieEtablissement,libelleVoieEtablissement,codePostalEtablissement,libelleCommuneEtablissement,libelleCommuneEtrangerEtablissement,distributionSpecialeEtablissement,codeCommuneEtablissement,codeCedexEtablissement,libelleCedexEtablissement,codePaysEtrangerEtablissement,libellePaysEtrangerEtablissement,identifiantAdresseEtablissement,coordonneeLambertAbscisseEtablissement,coordonneeLambertOrdonneeEtablissement,complementAdresse2Etablissement,numeroVoie2Etablissement,indiceRepetition2Etablissement,typeVoie2Etablissement,libelleVoie2Etablissement,codePostal2Etablissement,libelleCommune2Etablissement,libelleCommuneEtranger2Etablissement,distributionSpeciale2Etablissement,codeCommune2Etablissement,codeCedex2Etablissement,libelleCedex2Etablissement,codePaysEtranger2Etablissement,libellePaysEtranger2Etablissement,etatAdministratifEtablissement,enseigne1Etablissement,enseigne2Etablissement,enseigne3Etablissement,denominationUsuelleEtablissement,activitePrincipaleEtablissement,nomenclatureActivitePrincipaleEtablissement,caractereEmployeurEtablissement,geoloc

# We want to keep :
# - siren
# - dateCreationEtablissement
# - denominationUniteLegale
# - coordonneeLambertAbscisseEtablissement
# - coordonneeLambertOrdonneeEtablissement

newLines = []
i = 0
with open('./etablissements_geoloc.csv','r',encoding="utf8") as f:
    lines = f.readlines()
    header = lines[0].split(',')
    example = lines[5].split(',')
    j=0
    for headerName in header:
        print(j,":",headerName,example[j])
        j+=1
    
    for line in lines[1:]:
        i+=1
        data = line.split(',')
        newLines.append({
            "siren": data[0],
            "dateCreationEtablissement": data[4],
            "denominationUniteLegale": data[15],
            "coordonneeLambertAbscisseEtablissement": data[58],
            "coordonneeLambertOrdonneeEtablissement": data[59]
        })
        if i % 1000 == 0:
            print(f'{i/len(lines) * 100} %')

with open('./etablissements_geoloc_cleaned.csv', 'w',encoding='utf8') as f:

    f.write('siren,dateCreationEtablissement,denominationUniteLegale,coordonneeLambertAbscisseEtablissement,coordonneeLambertOrdonneeEtablissement\n')

    for line in newLines:
        f.write(f"{line['siren']},{line['dateCreationEtablissement']},{line['denominationUniteLegale']},{line['coordonneeLambertAbscisseEtablissement']},{line['coordonneeLambertOrdonneeEtablissement']}\n")

print('Done')


