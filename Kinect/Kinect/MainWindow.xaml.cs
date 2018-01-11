using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Kinect;


namespace Kinect
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {




        public ColorSkeletonData drawSkeleton { get; set; }



        public MainWindow()
        {
            InitializeComponent();
            this.drawSkeleton = new ColorSkeletonData();
            
        }


        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            this.drawSkeleton.InitializeSensorAndSkeleton(CnvSkeleton, imgCamera); 
        }





        //bij sluiten van het window wordt de kinect gestopt
        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            this.drawSkeleton.StopSensorAndSkeleton(); 
        }



        // Timer wordt gestart
        // Elke zoveel tijd wordt data over joints en boneorientation doorgestuurd
        private void btnStartRecord_Click(object sender, RoutedEventArgs e)
        {
            this.drawSkeleton.InitTimer();
        }


        //Timer wordt gestopt
        private void btnStopRecord_Click(object sender, RoutedEventArgs e)
        {
            this.drawSkeleton.StopTimer();
        }
    }
    }

