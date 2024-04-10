using System;
using System.Collections.Generic;
using System.IO;
using System.Numerics;
using MySql.Data.MySqlClient;

namespace ssd_screencity_dataengineering
{
    class Program
    {
        static int ProgressionSteps = 500000;
        static float MaxLines = 34636765;
        static void Main(string[] args)
        {
            List<string> data = new List<string>();
            var patchOfEtablissementFiles = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\etablissements_{i}.csv";
            var header = "";
            for (int i = 1; i < 4; i++)
            {
                string path = patchOfEtablissementFiles.Replace("{i}", i.ToString());
                using (StreamReader file = new StreamReader(path))
                {
                    string line;
                    //ignore the first line
                    header = file.ReadLine();
                    while ((line = file.ReadLine()) != null)
                    {
                        data.Add(line);
                    }
                }
            }

            Console.WriteLine($"There are {data.Count} lines in the files.");

            using(StreamWriter file = new StreamWriter(@"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\etablissements.csv"))
            {
                file.WriteLine(header);
                foreach (var line in data)
                {
                    file.WriteLine(line);
                }
            }

        }

        static void PrintProgression(int i)
        {
            if (i % Program.ProgressionSteps == 0)
            {
                Console.WriteLine(i / Program.MaxLines * 100.0 + "%");
            }
        } 

        public static int CountLinesInFile(string path)
        {
            int count = 0;
            using (StreamReader r = new StreamReader(path))
            {
                string line;
                while ((line = r.ReadLine()) != null)
                {
                    count++;
                }
            }

            Console.WriteLine("There are " + count + " lines in the file.");
            return count;
        }


        public static void LoadGeoloc()
        {
            string path = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8_sorted.csv";

            //TODO load geo loc in an array
        }

    }
}
