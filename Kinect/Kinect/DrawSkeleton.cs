using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Timers;
using System.Windows;
using System.Windows.Media;
using KinectCoordinateMapping;
using Microsoft.Kinect;
using static System.Net.Mime.MediaTypeNames;

namespace Kinect
{
    public class DrawSkeleton
    {
        //breedte van onze tekening
        public const float RenderWidth = 640.0f;


        //hoogte van onze tekening
        public const float RenderHeight = 480.0f;


        public const double JointThickness = 3;

        /// Thickness of body center ellipse
        public const double BodyCenterThickness = 10;

        /// Thickness of clip edge rectangles
        public const double ClipBoundsThickness = 10;

        /// Brush used to draw skeleton center point
        public readonly Brush centerPointBrush = Brushes.Blue;

        /// Brush used for drawing joints that are currently tracked
        public readonly Brush trackedJointBrush = new SolidColorBrush(Color.FromArgb(255, 68, 192, 68));

        /// Brush used for drawing joints that are currently inferred
        public readonly Brush inferredJointBrush = Brushes.Yellow;

        /// Pen used for drawing bones that are currently tracked
        public readonly Pen trackedBonePen = new Pen(Brushes.Green, 6);

        /// Pen used for drawing bones that are currently inferred
        public readonly Pen inferredBonePen = new Pen(Brushes.Gray, 1);

        //property voor kinectsensor 
        public KinectSensor Sensor;

        //array van skeletons 
        public Skeleton[] Skeletons;


        
        // drawing group voor skelet rendering output
        //dit zorgt ervoor dat meerdere tekeningen samengevoegd kunnen worden en als één tekening beschouwd kunnen worden
        public DrawingGroup drawingGroup;

        // drawing image die we zullen tonen
        public DrawingImage imageSource;

        System.Windows.Controls.Image image;


        private Timer timer;

        public int index;

        public void InitTimer()
        {
            Debug.WriteLine("-----Timer Started------");
            timer = new Timer(400);
            timer.Elapsed += Timer_Elapsed;
            timer.Enabled = true;
            timer.AutoReset = true;
        }

        public void StopTimer()
        {
            if(this.timer.Enabled == true)
            {
                this.timer.Dispose();
                this.index = 0;
                Debug.WriteLine("-----Timer Stopped-----");
            }

        }

        private void Timer_Elapsed(object sender, ElapsedEventArgs e)
        {


            index += 1;


                foreach (Skeleton skel in Skeletons)
            
                if (skel.TrackingState != null && skel.TrackingState == SkeletonTrackingState.Tracked)
                {



                    using (StreamWriter writer = new StreamWriter("D:\\BoneOrientationsTest.txt", true))
                    {
                        writer.WriteLine("-----------------" + index + "-----------------");

                        foreach (Joint joint in skel.Joints)
                        {


                            string jointname = joint.JointType.ToString();
                            string x = joint.Position.X.ToString();
                            string y = joint.Position.Y.ToString();
                            string z = joint.Position.Z.ToString();



                            string JointInformation = jointname + ": " + x + "/" + y + "/" + z + Environment.NewLine;

                            writer.WriteLine(JointInformation);


                            Debug.WriteLine(JointInformation);
                        }


                  
                    }
                }


        }




        public void InitializeSensorAndSkeleton(System.Windows.Controls.Image image1, System.Windows.Controls.Image image2)
        {
            // nieuwe drawing group maken
            this.drawingGroup = new DrawingGroup();

            // imagesource
            this.imageSource = new DrawingImage(this.drawingGroup);

            //imagesource linken aan onze image in xaml
            image1.Source = imageSource;

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
                    this.Skeletons = new Skeleton[skeletonFrame.SkeletonArrayLength];
                    skeletonFrame.CopySkeletonDataTo(this.Skeletons); // skelet informatie van het frame bemachtigen
                    foreach(Skeleton skel in Skeletons)
                    {
                        if(skel.TrackingState == SkeletonTrackingState.Tracked)
                        {
                            foreach(Joint joint in skel.Joints)
                            {
                                // 3D coordinates in meters
                                SkeletonPoint skeletonPoint = joint.Position;

                                // 2D coordinates in pixels
                                Point point = new Point();

                                
                                // Skeleton-to-Color mapping
                                ColorImagePoint colorPoint = Sensor.CoordinateMapper.MapSkeletonPointToColorPoint(skeletonPoint, ColorImageFormat.RgbResolution640x480Fps30);

                                point.X = colorPoint.X;
                                point.Y = colorPoint.Y;

                            }
                        }
                    }

                    DrawSkeletons();

                    
                }
            }
        }


        //Voor de trackingstate:
        // 1) tracked : geeft informatie terug over alle joints van het skelet
        // 2) poistiononly: geeft enkel informatie terug over de positie van het skelet

        private void DrawSkeletons()
        {
            using (DrawingContext dc = this.drawingGroup.Open())
            {
                ////transparante achtergrond tekenen
                //dc.DrawRectangle(Brushes.Black, null, new Rect(0.0, 0.0, RenderWidth, RenderHeight));

                if (Skeletons.Length != 0)
                {
                    foreach (Skeleton skel in Skeletons)
                    {
                        RenderClippedEdges(skel, dc);

                        if (skel.TrackingState == SkeletonTrackingState.Tracked)
                        {
                            this.DrawBonesAndJoints(skel, dc);
                        }
                        else if (skel.TrackingState == SkeletonTrackingState.PositionOnly)
                        {
                            dc.DrawEllipse(
                            this.centerPointBrush,
                            null,
                            this.SkeletonPointToScreen(skel.Position),
                            BodyCenterThickness,
                            BodyCenterThickness);
                        }
                    }
                }

                //zorgt ervoor dat we niet buiten het veld tekenen
                this.drawingGroup.ClipGeometry = new RectangleGeometry(new Rect(0.0, 0.0, RenderWidth, RenderHeight));
            }

        }



        // het skelet tekenen
        private void DrawBonesAndJoints(Skeleton skeleton, DrawingContext drawingContext)
        {
            // Render Torso
            this.DrawBone(skeleton, drawingContext, JointType.Head, JointType.ShoulderCenter);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.ShoulderLeft);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.ShoulderRight);
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderCenter, JointType.Spine);
            this.DrawBone(skeleton, drawingContext, JointType.Spine, JointType.HipCenter);
            this.DrawBone(skeleton, drawingContext, JointType.HipCenter, JointType.HipLeft);
            this.DrawBone(skeleton, drawingContext, JointType.HipCenter, JointType.HipRight);

            // Left Arm
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderLeft, JointType.ElbowLeft);
            this.DrawBone(skeleton, drawingContext, JointType.ElbowLeft, JointType.WristLeft);
            this.DrawBone(skeleton, drawingContext, JointType.WristLeft, JointType.HandLeft);

            // Right Arm
            this.DrawBone(skeleton, drawingContext, JointType.ShoulderRight, JointType.ElbowRight);
            this.DrawBone(skeleton, drawingContext, JointType.ElbowRight, JointType.WristRight);
            this.DrawBone(skeleton, drawingContext, JointType.WristRight, JointType.HandRight);

            // Left Leg
            this.DrawBone(skeleton, drawingContext, JointType.HipLeft, JointType.KneeLeft);
            this.DrawBone(skeleton, drawingContext, JointType.KneeLeft, JointType.AnkleLeft);
            this.DrawBone(skeleton, drawingContext, JointType.AnkleLeft, JointType.FootLeft);

            // Right Leg
            this.DrawBone(skeleton, drawingContext, JointType.HipRight, JointType.KneeRight);
            this.DrawBone(skeleton, drawingContext, JointType.KneeRight, JointType.AnkleRight);
            this.DrawBone(skeleton, drawingContext, JointType.AnkleRight, JointType.FootRight);

            // Render Joints
            foreach (Joint joint in skeleton.Joints)
            {
                Brush drawBrush = null;

                if (joint.TrackingState == JointTrackingState.Tracked)
                {
                    drawBrush = this.trackedJointBrush;
                }
                else if (joint.TrackingState == JointTrackingState.Inferred)
                {
                    drawBrush = this.inferredJointBrush;
                }

                if (drawBrush != null)
                {
                    drawingContext.DrawEllipse(drawBrush, null, this.SkeletonPointToScreen(joint.Position), JointThickness, JointThickness);
                }
            }
        }

        //beenderen tekenen

        private void DrawBone(Skeleton skeleton, DrawingContext drawingContext, JointType jointType0, JointType jointType1)

        {
            Joint joint0 = skeleton.Joints[jointType0];
            Joint joint1 = skeleton.Joints[jointType1];

            // If we can't find either of these joints, exit
            if (joint0.TrackingState == JointTrackingState.NotTracked ||
                joint1.TrackingState == JointTrackingState.NotTracked)
            {
                return;
            }

            // Don't draw if both points are inferred
            if (joint0.TrackingState == JointTrackingState.Inferred &&
                joint1.TrackingState == JointTrackingState.Inferred)
            {
                return;
            }

            // We assume all drawn bones are inferred unless BOTH joints are tracked
            Pen drawPen = this.inferredBonePen;
            if (joint0.TrackingState == JointTrackingState.Tracked && joint1.TrackingState == JointTrackingState.Tracked)
            {
                drawPen = this.trackedBonePen;
            }

            drawingContext.DrawLine(drawPen, this.SkeletonPointToScreen(joint0.Position), this.SkeletonPointToScreen(joint1.Position));
        }

        private Point SkeletonPointToScreen(SkeletonPoint skelpoint)
        {
            // Convert point to depth space.  
            // We are not using depth directly, but we do want the points in our 640x480 output resolution.
            DepthImagePoint depthPoint = this.Sensor.CoordinateMapper.MapSkeletonPointToDepthPoint(skelpoint, DepthImageFormat.Resolution640x480Fps30);
            ColorImagePoint colorPoint = this.Sensor.CoordinateMapper.MapSkeletonPointToColorPoint(skelpoint, ColorImageFormat.RgbResolution640x480Fps30);
            return new Point(depthPoint.X, depthPoint.Y);
        }

        private static void RenderClippedEdges(Skeleton skeleton, DrawingContext drawingContext)
        {
            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Bottom))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, RenderHeight - ClipBoundsThickness, RenderWidth, ClipBoundsThickness));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Top))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, RenderWidth, ClipBoundsThickness));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Left))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(0, 0, ClipBoundsThickness, RenderHeight));
            }

            if (skeleton.ClippedEdges.HasFlag(FrameEdges.Right))
            {
                drawingContext.DrawRectangle(
                    Brushes.Red,
                    null,
                    new Rect(RenderWidth - ClipBoundsThickness, 0, ClipBoundsThickness, RenderHeight));
            }
        }


    }
}
