using System;
using System.Diagnostics;
using System.IO;
using System.IO.MemoryMappedFiles;
using System.Threading;
using System.Text;
using System.Linq;

namespace SharedMemory
{
    class Program
    {
        static void Main(string[] args)
        {/*
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = "py";
            startInfo.Arguments = "C:/Users/User/Documents/C#/SharedMemory/SharedMemory/SharedMemory/main.py";

            startInfo.UseShellExecute = false;
            startInfo.CreateNoWindow = true;

            Process process = new Process();
            process.StartInfo = startInfo;

            process.Start();

            */

            try
            {
                MemoryMappedFile mmf = MemoryMappedFile.OpenExisting("testfile");

                //bool mutexCreated;
                //Mutex mutex = new Mutex(true, "testfilemutex", out mutexCreated);

                MemoryMappedViewStream stream = mmf.CreateViewStream();

                //BinaryWriter writer = new BinaryWriter(stream);
                //StreamReader reader_s = new StreamReader(stream);
                BinaryReader reader_b = new BinaryReader(stream);

                //int read_int = reader_b.ReadInt32();
                while (true)
                {
                    //Console.Clear();
                    stream.Position = 0;

                    byte[] bytes = reader_b.ReadBytes(8);
                    string output = "";

                    if (bytes.Length == 8)
                    {
                        //output = Encoding.UTF8.GetString(new ArraySegment<byte>(bytes, 4, 7));
                    }

                    Console.WriteLine($"[{String.Join(", ", bytes)}]  |  (Length: {bytes.Length})");
                    Console.WriteLine(output);

                    Thread.Sleep(10);
                }
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("File not found or already unlinked!");
                Environment.Exit(0);
            }
        }
    }
}
