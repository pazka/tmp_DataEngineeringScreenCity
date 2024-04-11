using System;
using System.Collections.Generic;
using System.IO;
using System.Numerics;
using MySql.Data.MySqlClient;

namespace ssd_screencity_dataengineering
{
    class Program
    {
        static void Main(string[] args)
        {
            StoreCsv();
        }

        static void StoreInSql(string[] args)
        {
            MySqlConnection myConnection;
            string myConnectionString;
            //set the correct values for your server, user, password and database name
            myConnectionString = "server=localhost;uid=root;pwd=root;database=data";

            try
            {
                myConnection = new MySqlConnection(myConnectionString);
                //open a connection
                myConnection.Open();
                AssignCsvToTable(myConnection);
            }
            catch (MySqlException ex)
            {
                Console.WriteLine(ex.Message);
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

        public static void AssignCsvToTable(MySqlConnection myConnection)
        {
            string path = @"C:\Users\Alexa\Documents\Projects\Alessia\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv";
            // Read the file and display it line by line.  
            StreamReader file = new StreamReader(path);
            string line;
            var i = 0;
            file.ReadLine(); // skip the first line
            do 
            {
                if(i % 1000 == 0)
                {
                    Console.WriteLine( i / 153996 *100 + "%");
                }

                line = file.ReadLine();
                string[] lineArray = line.Split(";");
                AddNewLineInTable(lineArray, myConnection);
                i++;
            }while (line != null);

            Console.WriteLine("There are " + i + " lines in the file.");
            file.Close();
         }

         
        public static void StoreCsv()
        {
            string path = @"C:\Users\Alexa\Documents\Projects\Alessia\Seine-Saint-Denis_ScreenCityDataEngineering\ssd_screencity_dataengineering\data\GeolocalisationEtablissement_Sirene_pour_etudes_statistiques_utf8.csv";
            float maxLines = 34636765 ;
            CountLinesInFile(path);

            StreamReader file = new StreamReader(path);
            string[][] dataLines = new string[34636765][]; // 34M lines
            SortedDictionary<BigInteger,int> linesIndexes = new SortedDictionary<BigInteger,int>();

            int i = 0;
            file.ReadLine(); // skip the first line
            string line;
            do 
            {
                line = file.ReadLine();
                
                if (i % 10000 == 0)
                {
                    Console.WriteLine((i / maxLines ) * 100 + "%");
                }

                string[] lineArray = line.Split(";");
                BigInteger lineIdx = BigInteger.Parse(lineArray[0]);
                dataLines[i] = lineArray;
                linesIndexes.Add(lineIdx, i);

                i++;
            }while (line != null);

            Console.WriteLine("Went up to " + i + " lines in the file.");
            file.Close();
        }

        public static void AddNewLineInTable(string[] line,MySqlConnection myConnection)
        {
            // create a MySQL command and set the SQL statement with parameters
            MySqlCommand myCommand = new MySqlCommand();
            myCommand.Connection = myConnection;
            myCommand.CommandText = @"INSERT INTO geoloc (siret, x, y, qualite_xy, epsg, plg_qp, plg_iris, plg_zus, plg_qva, plg_code_commune, distance_precision, qualite_qp, qualite_iris, qualite_zus, qualite_qva, y_latitude, x_longitude) VALUES (@siret, @x, @y, @qualite_xy, @epsg, @plg_qp, @plg_iris, @plg_zus, @plg_qva, @plg_code_commune, @distance_precision, @qualite_qp, @qualite_iris, @qualite_zus, @qualite_qva, @y_latitude, @x_longitude);";
            myCommand.Parameters.AddWithValue("@siret", line[0]);
            myCommand.Parameters.AddWithValue("@x", line[1]);
            myCommand.Parameters.AddWithValue("@y", line[2]);
            myCommand.Parameters.AddWithValue("@qualite_xy", line[3]);
            myCommand.Parameters.AddWithValue("@epsg", line[4]);
            myCommand.Parameters.AddWithValue("@plg_qp", line[5]);
            myCommand.Parameters.AddWithValue("@plg_iris", line[6]);
            myCommand.Parameters.AddWithValue("@plg_zus", line[7]);
            myCommand.Parameters.AddWithValue("@plg_qva", line[8]);
            myCommand.Parameters.AddWithValue("@plg_code_commune", line[9]);
            myCommand.Parameters.AddWithValue("@distance_precision", line[10]);
            myCommand.Parameters.AddWithValue("@qualite_qp", line[11]);
            myCommand.Parameters.AddWithValue("@qualite_iris", line[12]);
            myCommand.Parameters.AddWithValue("@qualite_zus", line[13]);
            myCommand.Parameters.AddWithValue("@qualite_qva", line[14]);
            myCommand.Parameters.AddWithValue("@y_latitude", line[15]);
            myCommand.Parameters.AddWithValue("@x_longitude", line[16]);

            // execute the command
            myCommand.ExecuteNonQuery();
        }
    }
}
