using System;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace PythonProcessing
{
    public delegate void StreamReciever(string message);

    public class DataStream
    {
        //StreamWriter writer;
        StreamReader reader;
        string result;
        string file_path;
        string python_path;
        public int frame;
        //public event StreamReciever OnMessageRecieved;

        public DataStream(bool create_window, string file_path, string python_path)
        {
            this.file_path = file_path;
            this.python_path = python_path;
        }

        public StreamReader Start()
        {
            ProcessStartInfo start = new ProcessStartInfo();

            start.FileName = python_path;
            start.Arguments = string.Format("{0}", file_path);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            //start.RedirectStandardInput = true;
            start.CreateNoWindow = true;

            Process process = new Process();
            process.StartInfo = start;
            process.PriorityBoostEnabled = true;
            //writer = process.StandardInput;
            /*
            process.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data))
                {
                    UnityEngine.Debug.Log($"Data recieved! at {frame}");
                    OnMessageRecieved("Data: " + e.Data);
                }
            });
            */
            process.Start();
            reader = process.StandardOutput;

            //process.BeginOutputReadLine();
            //process.PriorityClass = ProcessPriorityClass.High;
            return reader;
            //Request(request);
        }
        /*
        public Task Request(string request)
        {
            if (writer == null) return null;
            else
            {

                return Task.Factory.StartNew(() =>
                {
                    while (true)
                    {
                        //writer.WriteLine(request);
                        result = null;

                        while (result == null || result.Length == 0)
                        { result = reader.ReadLine(); }

                        Recieved(result);
                        //UnityEngine.Debug.Log($"Getting: {result} at frame {Time.frameCount.ToString()}");
                    }
                });
            }
        }

        void Recieved(string res)
        {
            //UnityEngine.Debug.Log(res);
            OnMessageRecieved(res);
        }

        public void Sync()
        {
            result = reader.ReadLine();
            if (result != null && result.Length != 0)
            { OnMessageRecieved(result); }
        }*/
    }

    public static class Extensions
    {
        public static Vector2Int toVector2(this string rString)
        {
            string[] temp = rString.Substring(2, rString.Length - 3).Split(',');
            int x = int.Parse(temp[0]);
            int y = int.Parse(temp[1]);
            Vector2Int rValue = new Vector2Int(x, y);
            return rValue;
        }
    }
}