# get a portion of the file etablissements_geoloc_cleaned_with_count_in_ssd.csv
# must go through all the file, not just th estart

percentage = 0.1

with open('etablissements_geoloc_cleaned_with_count_in_ssd.csv', 'r') as src_file:
    with open('small_etablissements_geoloc_cleaned_with_count_in_ssd.csv', 'w') as dest_file:
        for i, line in enumerate(src_file):
            if i % (1/percentage) == 0:
                dest_file.write(line)
