using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Timers;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;
using Kinect.Model;
using KinectCoordinateMapping;
using Microsoft.Kinect;
using uPLibrary.Networking.M2Mqtt;
using Newtonsoft.Json;
using static System.Net.Mime.MediaTypeNames;

namespace Kinect
{
    public class ColorSkeletonData
    {
       

        //property voor kinectsensor 
        public KinectSensor Sensor;

        //array van skeletons 
        public Skeleton[] Skeletons;


       // image voor colorstream
        System.Windows.Controls.Image image;


        //canvas om skelet op te tekenen
        System.Windows.Controls.Canvas canvas;

        //timer
        private Timer timer;

        public MqttClient client;

        //dictionary voor het tekenen van de bones (zal joint name en zijn position bevatten)
        public Dictionary<string, Point> dictionary = new Dictionary<string, Point>();


        //timer starten
        public void InitTimer()
        {
            Debug.WriteLine("-----Timer Started------");
            timer = new Timer(600);
            timer.Elapsed += Timer_Elapsed;
            timer.Enabled = true;
            //timer.AutoReset = true;
        }

        //timer stoppen
        public void StopTimer()
        {
            if(this.timer.Enabled == true)
            {
                this.timer.Dispose();
                Debug.WriteLine("-----Timer Stopped-----");
            }

            else
            {
                return;
            }

        }

        public void InitMqtt()
        {
            this.client = new MqttClient(IPAddress.Parse("172.30.252.101"));
            client.Connect(Guid.NewGuid().ToString());
        }


        //event na aflopen timer
        //schrijft iedere x seconden jointpositions weg
        private void Timer_Elapsed(object sender, ElapsedEventArgs e)
        {


                foreach (Skeleton skel in Skeletons)
            
                if (skel.TrackingState != null && skel.TrackingState == SkeletonTrackingState.Tracked)
                {



                    
                        List<JointCoordinates> jointcoordinates = new List<JointCoordinates>();

                        foreach (Joint joint in skel.Joints)
                        {

                            JointCoordinates jointcoordinate = new JointCoordinates();

                            jointcoordinate.JointName = joint.JointType.ToString();
                            List<float> floats = new List<float>();
                            floats.Add(joint.Position.X);
                            floats.Add(joint.Position.Y);
                            floats.Add(joint.Position.Z);
                            jointcoordinate.Coordinates = floats;
                            jointcoordinates.Add(jointcoordinate);

                           

                        }

                        string json = JsonConvert.SerializeObject(jointcoordinates);

                        client.Publish("/Sandro", Encoding.UTF8.GetBytes(json));




                    
                }


        }



        public void InitializeSensorAndSkeleton(System.Windows.Controls.Canvas canvas, System.Windows.Controls.Image image2)
        {
          

            this.canvas = canvas;

            this.image = image2;

            // zoek de geconnecteerde kinectsensor en stopt hem in onze property
            foreach (var potentialSensor in KinectSensor.KinectSensors)
            {
                if (potentialSensor.Status == KinectStatus.Connected)
                {
                    this.Sensor = potentialSensor;
                    break;
                }
            }


            if (this.Sensor != null)
            {


                
                //kleur aanzetten
                this.Sensor.ColorStream.Enable();

                // dit start skeletontracking
                this.Sensor.SkeletonStream.Enable();




                
                //event op colorstream
                Sensor.ColorFrameReady += Sensor_ColorFrameReady;

                //event op skeletonstream
                Sensor.SkeletonFrameReady += Sensor_SkeletonFrameReady;


                //sensor proberen te starten - best nog iets doen wanneer hij bv niet zou starten 
                try
                {
                    this.Sensor.Start();
                }
                catch (IOException)
                {
                    this.Sensor = null;
                }

            }
        }

        private void Sensor_ColorFrameReady(object sender, ColorImageFrameReadyEventArgs e)
        {
            using (var frame = e.OpenColorImageFrame())
            {
                if (frame != null)
                {
                    
                    this.image.Source = frame.ToBitmap();
                   
                }
            }
        }

        public void StopSensorAndSkeleton()
        {
            if (this.Sensor != null)
            {
                this.Sensor.Stop();
            }
        }

        // eventhandler voor skeletonframe
        private void Sensor_SkeletonFrameReady(object sender, SkeletonFrameReadyEventArgs e)
        {

            this.Skeletons = new Skeleton[0];
            

            using (SkeletonFrame skeletonFrame = e.OpenSkeletonFrame()) //skelet openen
            {
                if (skeletonFrame != null) // checken of een frame beschikbaar is 
                {

                    canvas.Children.Clear();

                    this.Skeletons = new Skeleton[skeletonFrame.SkeletonArrayLength];
                    skeletonFrame.CopySkeletonDataTo(this.Skeletons); // skelet informatie van het frame bemachtigen
                    foreach(Skeleton skel in Skeletons)
                    {

                        if (skel.TrackingState == SkeletonTrackingState.Tracked)
                        {
                            Dictionary<string, Point> dictionary = new Dictionary<string, Point>();


                            foreach (Joint joint in skel.Joints)
                            {
                                //3D coordinaten in meter
                                SkeletonPoint skeletonPoint = joint.Position;

                                // 2D coordinaten in pixels
                                Point point = new Point();

                                
                                // Skelet naar color mapping
                                ColorImagePoint colorPoint = Sensor.CoordinateMapper.MapSkeletonPointToColorPoint(skeletonPoint, ColorImageFormat.RgbResolution640x480Fps30);

                                point.X = colorPoint.X;
                                point.Y = colorPoint.Y;

                                string type = joint.JointType.ToString();
                                Point point2 = point;


                                dictionary.Add(type, point2);


                                Ellipse ellipse = new Ellipse
                                {
                                    Fill = Brushes.Red,
                                    Width = 10,
                                    Height = 10
                                };

                                

                                Canvas.SetLeft(ellipse, point.X - ellipse.Width / 2);
                                Canvas.SetTop(ellipse, point.Y - ellipse.Height / 2);

                                canvas.Children.Add(ellipse);
                                

                            }

                            DrawBones(dictionary);

                        }
                    }


                    
                }
            }
        }

        // tekent de bones tussen de verschillende joints adhv x,y van joint1 & joint2
        public void DrawBones(Dictionary<string, Point> dictionary)
        {
            
            Line line = new Line();
            line.Stroke = Brushes.Green;
            line.StrokeThickness = 2;

            line.X1 = dictionary["Head"].X;
            line.Y1 = dictionary["Head"].Y;
            line.X2 = dictionary["ShoulderCenter"].X;
            line.Y2 = dictionary["ShoulderCenter"].Y;

            canvas.Children.Add(line);

            Line line2 = new Line();
            line2.Stroke = Brushes.Green;
            line2.StrokeThickness = 2;

            line2.X1 = dictionary["ShoulderCenter"].X;
            line2.Y1 = dictionary["ShoulderCenter"].Y;
            line2.X2 = dictionary["ShoulderLeft"].X;
            line2.Y2 = dictionary["ShoulderLeft"].Y;

            canvas.Children.Add(line2);

            Line line3 = new Line();
            line3.Stroke = Brushes.Green;
            line3.StrokeThickness = 2;

            line3.X1 = dictionary["ShoulderCenter"].X;
            line3.Y1 = dictionary["ShoulderCenter"].Y;
            line3.X2 = dictionary["ShoulderRight"].X;
            line3.Y2 = dictionary["ShoulderRight"].Y;

            canvas.Children.Add(line3);

            Line line4 = new Line();
            line4.Stroke = Brushes.Green;
            line4.StrokeThickness = 2;

            line4.X1 = dictionary["ShoulderCenter"].X;
            line4.Y1 = dictionary["ShoulderCenter"].Y;
            line4.X2 = dictionary["Spine"].X;
            line4.Y2 = dictionary["Spine"].Y;

            canvas.Children.Add(line4);



            Line line5 = new Line();
            line5.Stroke = Brushes.Green;
            line5.StrokeThickness = 2;

            line5.X1 = dictionary["Spine"].X;
            line5.Y1 = dictionary["Spine"].Y;
            line5.X2 = dictionary["HipCenter"].X;
            line5.Y2 = dictionary["HipCenter"].Y;

            canvas.Children.Add(line5);


            Line line6 = new Line();
            line6.Stroke = Brushes.Green;
            line6.StrokeThickness = 2;

            line6.X1 = dictionary["HipCenter"].X;
            line6.Y1 = dictionary["HipCenter"].Y;
            line6.X2 = dictionary["HipLeft"].X;
            line6.Y2 = dictionary["HipLeft"].Y;

            canvas.Children.Add(line6);


            Line line7 = new Line();
            line7.Stroke = Brushes.Green;
            line7.StrokeThickness = 2;

            line7.X1 = dictionary["HipCenter"].X;
            line7.Y1 = dictionary["HipCenter"].Y;
            line7.X2 = dictionary["HipRight"].X;
            line7.Y2 = dictionary["HipRight"].Y;

            canvas.Children.Add(line7);



            Line line8 = new Line();
            line8.Stroke = Brushes.Green;
            line8.StrokeThickness = 2;

            line8.X1 = dictionary["ShoulderLeft"].X;
            line8.Y1 = dictionary["ShoulderLeft"].Y;
            line8.X2 = dictionary["ElbowLeft"].X;
            line8.Y2 = dictionary["ElbowLeft"].Y;

            canvas.Children.Add(line8);



            Line line9 = new Line();
            line9.Stroke = Brushes.Green;
            line9.StrokeThickness = 2;

            line9.X1 = dictionary["ElbowLeft"].X;
            line9.Y1 = dictionary["ElbowLeft"].Y;
            line9.X2 = dictionary["WristLeft"].X;
            line9.Y2 = dictionary["WristLeft"].Y;

            canvas.Children.Add(line9);



            Line line10 = new Line();
            line10.Stroke = Brushes.Green;
            line10.StrokeThickness = 2;

            line10.X1 = dictionary["WristLeft"].X;
            line10.Y1 = dictionary["WristLeft"].Y;
            line10.X2 = dictionary["HandLeft"].X;
            line10.Y2 = dictionary["HandLeft"].Y;

            canvas.Children.Add(line10);




            Line line11 = new Line();
            line11.Stroke = Brushes.Green;
            line11.StrokeThickness = 2;

            line11.X1 = dictionary["ShoulderRight"].X;
            line11.Y1 = dictionary["ShoulderRight"].Y;
            line11.X2 = dictionary["ElbowRight"].X;
            line11.Y2 = dictionary["ElbowRight"].Y;

            canvas.Children.Add(line11);


            Line line12 = new Line();
            line12.Stroke = Brushes.Green;
            line12.StrokeThickness = 2;

            line12.X1 = dictionary["ElbowRight"].X;
            line12.Y1 = dictionary["ElbowRight"].Y;
            line12.X2 = dictionary["WristRight"].X;
            line12.Y2 = dictionary["WristRight"].Y;

            canvas.Children.Add(line12);


            Line line13 = new Line();
            line13.Stroke = Brushes.Green;
            line13.StrokeThickness = 2;

            line13.X1 = dictionary["WristRight"].X;
            line13.Y1 = dictionary["WristRight"].Y;
            line13.X2 = dictionary["HandRight"].X;
            line13.Y2 = dictionary["HandRight"].Y;

            canvas.Children.Add(line13);



            Line line14 = new Line();
            line14.Stroke = Brushes.Green;
            line14.StrokeThickness = 2;

            line14.X1 = dictionary["HipLeft"].X;
            line14.Y1 = dictionary["HipLeft"].Y;
            line14.X2 = dictionary["KneeLeft"].X;
            line14.Y2 = dictionary["KneeLeft"].Y;

            canvas.Children.Add(line14);


            Line line15 = new Line();
            line15.Stroke = Brushes.Green;
            line15.StrokeThickness = 2;

            line15.X1 = dictionary["KneeLeft"].X;
            line15.Y1 = dictionary["KneeLeft"].Y;
            line15.X2 = dictionary["AnkleLeft"].X;
            line15.Y2 = dictionary["AnkleLeft"].Y;

            canvas.Children.Add(line15);


            Line line16 = new Line();
            line16.Stroke = Brushes.Green;
            line16.StrokeThickness = 2;

            line16.X1 = dictionary["AnkleLeft"].X;
            line16.Y1 = dictionary["AnkleLeft"].Y;
            line16.X2 = dictionary["FootLeft"].X;
            line16.Y2 = dictionary["FootLeft"].Y;

            canvas.Children.Add(line16);


            Line line17 = new Line();
            line17.Stroke = Brushes.Green;
            line17.StrokeThickness = 2;

            line17.X1 = dictionary["HipRight"].X;
            line17.Y1 = dictionary["HipRight"].Y;
            line17.X2 = dictionary["KneeRight"].X;
            line17.Y2 = dictionary["KneeRight"].Y;

            canvas.Children.Add(line17);


            Line line18 = new Line();
            line18.Stroke = Brushes.Green;
            line18.StrokeThickness = 2;

            line18.X1 = dictionary["KneeRight"].X;
            line18.Y1 = dictionary["KneeRight"].Y;
            line18.X2 = dictionary["AnkleRight"].X;
            line18.Y2 = dictionary["AnkleRight"].Y;

            canvas.Children.Add(line18);


            Line line19 = new Line();
            line19.Stroke = Brushes.Green;
            line19.StrokeThickness = 2;

            line19.X1 = dictionary["AnkleRight"].X;
            line19.Y1 = dictionary["AnkleRight"].Y;
            line19.X2 = dictionary["FootRight"].X;
            line19.Y2 = dictionary["FootRight"].Y;

            canvas.Children.Add(line19);
      
            dictionary.Clear();

        }

    }
}
