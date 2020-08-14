using System;
using System.Collections;
using System.Collections.Generic;
using Streaming;
using UnityEngine;
using Debug = UnityEngine.Debug;

public class Controller : MonoBehaviour
{
    public int test;
    public int pos_x;
    public Vector3 left;
    public Vector3 right;
    BinaryStream stream;

    void Start()
    {
        MotionTracking.python_path = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python38-32\\python.exe";
        MotionTracking.file_path = $"{Environment.CurrentDirectory}\\Assets\\Scripts\\Python\\streaming.py";

        stream = MotionTracking.Start(false);

        stream.BytesRecieved += Stream_OnBytesRecieved;
    }

    private void Stream_OnBytesRecieved(object e, BytesRecievedEventArgs args)
    {
        Debug.Log($"Bytes recieved: {args.hand_l_pos_x}");
        pos_x = args.hand_l_pos_x;
    }

    void Update()
    {
        test = stream.tst;
        left = MotionTracking.hands.left;
        right = MotionTracking.hands.right;
    }
}
