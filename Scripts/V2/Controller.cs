using System;
using System.Collections;
using System.Collections.Generic;
using Streaming;
using UnityEngine;
using UnityEngine.UI;
using Debug = UnityEngine.Debug;

public class Controller : MonoBehaviour
{
    public byte[] settings;
    public string output;
    public int test;
    public int pos_x;
    public Vector3 left;
    public Vector3 right;
    BinaryStream stream;
    Text text;

    void Start()
    {
        text = GameObject.Find("Text").GetComponent<Text>();

        MotionTracking.python_path = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python38-32\\python.exe";
        MotionTracking.file_path = $"{Environment.CurrentDirectory}\\Assets\\motion-tracking\\Scripts\\Python\\main.py";

        stream = MotionTracking.Start(false, settings: settings);

        stream.BytesRecieved += Stream_OnBytesRecieved;

        Debug.Log($"{MotionTracking.python_path} {MotionTracking.file_path}");
    }

    private void Stream_OnBytesRecieved(object e, BytesRecievedEventArgs args)
    {
        //Debug.Log($"Bytes recieved: {args.hand_l_pos_x}");
        pos_x = args.hand_l_pos_x;
    }

    void Update()
    {
        output = stream.output;
        text.text = stream.output;
        test = stream.tst;
        left = MotionTracking.hands.left;
        right = MotionTracking.hands.right;
    }

    private void OnApplicationQuit()
    {
        stream.StopListening();
    }
}
