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
            StoreCsv();
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


        public static void StoreCsv()
        {
            string path = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv";

            CountLinesInFile(path);
            string[][] dataLines = new string[34636765][]; // 34M lines
            SortedDictionary<string, int> linesIndexes = new SortedDictionary<string, int>();

            using (StreamReader file = new StreamReader(path))
            {
                int i = 0;
                file.ReadLine(); // skip the first line

                string line = file.ReadLine();
                Console.WriteLine("Reading file...");
                do
                {
                    PrintProgression(i);

                    string[] lineArray = line.Split(";");
                    string lineIdx = lineArray[0];
                    dataLines[i] = lineArray;
                    linesIndexes.Add(lineIdx, i);

                    line = file.ReadLine();
                    i++;
                } while (line != null);

                Console.WriteLine("Went up to " + i + " lines in the file.");
            }

            WriteSortedCSV(dataLines, linesIndexes);
        }

        public static void WriteSortedCSV(string[][] dataLines, SortedDictionary<string, int> linesIndexes)
        {
            string path = @"C:\Users\Pazka\Documents\Code\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8_sorted.csv";
            int i = 0;
            using (StreamWriter file = new StreamWriter(path))
            {
                Console.WriteLine("Writing to file...");

                foreach (var lineIdx in linesIndexes)
                {
                    PrintProgression(i);
                    string[] line = dataLines[lineIdx.Value];
                    string lineStr = string.Join(";", line);
                    file.WriteLine(lineStr);
                }
            }

            Console.WriteLine("Wrote " + i + " lines in the file.");
        }
    }
}
