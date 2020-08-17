using System;
using System.Diagnostics;
using System.IO;
using System.IO.MemoryMappedFiles;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using Debug = UnityEngine.Debug;

namespace Streaming
{
    public static class MotionTracking
    {
        //public struct Hand { public Vector3 position; }
        public struct Hands
        {
            public Vector3 left;
            public Vector3 right;
            public int tracked;
        }

        public static string python_path;
        public static string file_path;

        static bool read
        {
            get { return true; }
            set { }
        }

        static Process process;
        static BinaryStream stream;
        public static Hands hands;

        public static BinaryStream Start(bool execute_async = true, bool listen_on_start = true)
        {
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.FileName = python_path;
            processStartInfo.Arguments = file_path;
            processStartInfo.UseShellExecute = false;
            processStartInfo.RedirectStandardError = true;
            processStartInfo.CreateNoWindow = true;

            process = new Process();
            process.StartInfo = processStartInfo;
            process.ErrorDataReceived += Process_ErrorDataReceived;

            if (execute_async)
            {
                Task.Run(() => process.Start());
            }
            else { process.Start(); }

            stream = new BinaryStream(process);
            stream.BytesRecieved += Stream_BytesRecieved;

            if (listen_on_start) stream.ListenForBytes();

            return stream;
        }

        private static void Stream_BytesRecieved(object source, BytesRecievedEventArgs args)
        {
            hands.left.x = args.hand_l_pos_x;
            hands.left.y = args.hand_l_pos_y;

            hands.right.x = args.hand_r_pos_x;
            hands.right.y = args.hand_r_pos_y;
        }

        private static void Process_ErrorDataReceived(object sender, DataReceivedEventArgs e)
        {
            Debug.Log($"Error: {e.Data}");
        }
    }

    public class BinaryStream
    {
        public delegate void BytesRecievedEventHandler(object source, BytesRecievedEventArgs args);
        public event BytesRecievedEventHandler BytesRecieved;
        public int tst = 1;
        public string output;

        MemoryMappedViewStream stream;
        BinaryReader reader;
        //StreamReader streamReader;
        Process process;
        int byte_length;
        bool quit = false;

        public BinaryStream(Process process, string mmf_name = "motion_tracking_data_stream", int byte_length = 6)
        {
            //MemoryMappedFile mmf = MemoryMappedFile.OpenExisting(mmf_name);
            MemoryMappedFile mmf = MemoryMappedFile.CreateOrOpen(mmf_name, byte_length);

            stream = mmf.CreateViewStream();
            reader = new BinaryReader(stream);
            //streamReader = output;
            this.process = process;
            this.byte_length = byte_length;
        }

        public async void ListenForBytes()
        {
            while (!quit)
            {
                await Task.Run(() => CheckForBytes());
            }
        }

        public void StopListening() { quit = true; }

        void CheckForBytes()
        {
            BytesRecievedEventArgs args = new BytesRecievedEventArgs();

            // Core code here
            stream.Position = 0;
            byte[] bytes = reader.ReadBytes(byte_length);
            output = $"[{String.Join(",\t", bytes)}]\t|\t(Length: {bytes.Length})\t|  (running: {!process.HasExited})";
            //if (streamReader.HasExited) Debug.Log(streamReader.e);
            stream.Position = 0;

            args.read =         reader.ReadBoolean();
            args.hand_l_pos_x = reader.ReadInt32();
            args.hand_l_pos_y = reader.ReadInt32();
            args.hand_r_pos_x = reader.ReadInt32();
            args.hand_r_pos_y = reader.ReadInt32();
            args.tracked =      reader.ReadInt32();

            OnBytesRecieved(args);
            tst++;

            //Thread.Sleep(100);
        }
        
        protected virtual void OnBytesRecieved(BytesRecievedEventArgs args)
        {
            if (BytesRecieved != null)
            {
                BytesRecieved(this, args);
            }
        }
    }

    public class BytesRecievedEventArgs : EventArgs
    {
        public bool read { get; set; }
        public int hand_l_pos_x { get; set; }
        public int hand_l_pos_y { get; set; }
        public int hand_r_pos_x { get; set; }
        public int hand_r_pos_y { get; set; }
        public int tracked { get; set; }
    }
}