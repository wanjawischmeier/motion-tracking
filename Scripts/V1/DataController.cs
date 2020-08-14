using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PythonProcessing;
using System;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using UnityEngine.UI;
using System.IO;
using System.Threading;
using Streaming;

public class DataController : MonoBehaviour
{
    DataStream stream;
    StreamReader reader;
    Process process;
    public string request;
    public string output;
    public int frame;
    public Vector2Int asVector2;
    public Text text;

    void Start()
    {
        stream = new DataStream(true, $"{Application.dataPath}/Scripts/Python/main.py", $"{Application.dataPath}/Scripts/Python/Installation/python.exe");
        //stream.OnMessageRecieved += Rec;
        reader = stream.Start();
        Debug.Log("Waiting for response...");

        //while (true) Console.ReadKey();
        /*
        do
        {
            Debug.Log("[C# Request]\t|  >>> ");
            inp = Console.ReadLine();

            string result = stream.Request(inp);
            Debug.Log("[C# Request]\t|  Result:\t|  " + result + "\n");

        } while (inp != "exit");*/
        //Thread.CurrentThread.Priority = System.Threading.ThreadPriority.Highest;
    }

    void Update()
    {
        Debug.Log("Update start");
        frame = Time.frameCount;
        stream.frame = frame;
        string output = reader.ReadLine();
        Rec(output);
        text.text = $"Frame: {frame} | Out: {output}";
        Debug.Log("Update end");
        //stream.Sync();
        //stream.Request(request);
        //Debug.Log("[C# Request]\t|  Result:\t|  " + result + "\n");

    }

    private void Rec(string message)
    {
        Debug.Log($"message {frame}");
        output = message;
        text.text = message;
        if (message[0] == 't')
        {
            asVector2 = message.toVector2();
        }
        //Debug.Log("[C# Event]\t|  Recieved:\t|  " + message);
    }
}
