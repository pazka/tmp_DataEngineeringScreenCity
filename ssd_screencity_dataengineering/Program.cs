using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Numerics;
using MySql.Data.MySqlClient;
using Org.BouncyCastle.Asn1;
using Org.BouncyCastle.Tls.Crypto.Impl;

namespace ssd_screencity_dataengineering
{
    class Program
    {
        static void Main(string[] args)
        {
            string geoLocPath = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8_sorted.csv";

            using (StreamReader r = new StreamReader(geoLocPath))
            {
                Console.WriteLine("Reading geoloc file");
                Console.WriteLine("Header: " + r.ReadLine());
            }
            geoLocPath = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv";

            using (StreamReader r = new StreamReader(geoLocPath))
            {
                Console.WriteLine("geoloc file header");
                Console.WriteLine("Header: " + r.ReadLine());
            }
            string pathSireneWithoutGeoloc = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\etablissements.csv";

            using (StreamReader r = new StreamReader(pathSireneWithoutGeoloc))
            {
                Console.WriteLine("Reading sirene file");
                Console.WriteLine("Header: " + r.ReadLine());
                Console.WriteLine("Data: " + r.ReadLine());
            }

            string[] sireneGeoLoc = new string[34636763];

            LoadData(sireneGeoLoc);


            string pathSireneWithGeoloc = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\etablissements_geoloc.csv";
            // Load sirene without geoloc
            using (StreamWriter w = new StreamWriter(pathSireneWithGeoloc))
            {
                using (StreamReader r = new StreamReader(pathSireneWithoutGeoloc))
                {
                    string sireneWithoutGeoloc;
                    r.ReadLine(); // Skip header
                    int i = 0;
                    int found = 0;
                    int notFound = 0;

                    while ((sireneWithoutGeoloc = r.ReadLine()) != null)
                    {

                        if (i++ % 1000 == 0)
                        {
                            Console.WriteLine($"Processed {i} items : {found} found, {notFound} not found");
                        }

                        var index = FindIndexOfGeoLoc(sireneWithoutGeoloc, sireneGeoLoc);

                        if (index == -1)
                        {
                            notFound++;
                            continue;
                        }
                        else
                        {
                            found++;

                            var newLine = $"{sireneWithoutGeoloc},{sireneGeoLoc[index]}";
                            w.WriteLine(newLine);
                        }

                    }
                }
            }
        }

        static void LoadData(string[] sireneGeoLoc)
        {
            // Load geoloc
            string geoLocPath = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8_sorted.csv";

            using (StreamReader r = new StreamReader(geoLocPath))
            {
                string line;
                r.ReadLine(); // Skip header
                int i = 0;

                while ((line = r.ReadLine()) != null)
                {
                    sireneGeoLoc[i++] = line;
                }

                Console.WriteLine($"Geoloc loaded {sireneGeoLoc.Length} items");
            }
        }

        static int FindIndexOfGeoLoc(string sireneWithoutGeoloc, string[] siretGeoLoc)
        {
            //find using binary search

            var siretToFind = sireneWithoutGeoloc.Substring(0, 9);

            int minIndex = 0;
            int maxIndex = siretGeoLoc.Length - 1;

            while (minIndex <= maxIndex)
            {
                int middleIndex = (minIndex + (int)Math.Floor((maxIndex - minIndex) / 2.0));

                var middleSiret = siretGeoLoc[middleIndex].Substring(0, 9);

                if (middleSiret == siretToFind)
                {
                    return middleIndex;
                }
                else if (middleSiret.CompareTo(siretToFind) < 0)
                {
                    minIndex = middleIndex + 1;
                }
                else
                {
                    maxIndex = middleIndex - 1;
                }
            }

            return -1;
        }
    }
}
