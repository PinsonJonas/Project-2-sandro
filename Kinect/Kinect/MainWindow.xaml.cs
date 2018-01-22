using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
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

        public List<Model.Files> files { get; set; }

        public MainWindow()
        {
            InitializeComponent();
            this.drawSkeleton = new ColorSkeletonData();
            this.files = this.drawSkeleton.ReadFiles();
            lvwLibrary.ItemsSource = files;
            
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
            //mqttip & subject meegeven voor verificatie

            if (TxbSubject.Text != "") 
                {
                    drawSkeleton.InitMqtt(TxbIp.Text, TxbSubject.Text);
                    if (drawSkeleton.MqttConnected == false)
                    {
                        MessageBox.Show("We konden niet verbinden met het ingegeven ip adres. Probeer opnieuw");
                    }
                }

                else
            {
                MessageBox.Show("Gelieve een correcte topic op te geven.");

            }


        }


        //Timer wordt gestopt
        private void btnStopRecord_Click(object sender, RoutedEventArgs e)
        {
            if(drawSkeleton.timer.Enabled == true)
            {
                this.drawSkeleton.StopTimer();
                grdPopup.Visibility = Visibility.Visible;
            }

        }

        private void lvwLibrary_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            Debug.WriteLine("Werd verstuurd");
            Model.Files file = lvwLibrary.SelectedItem as Model.Files;
            drawSkeleton.client.Publish(TxbSubject.Text, Encoding.UTF8.GetBytes(file.Content));



        }

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            grdPopup.Visibility = Visibility.Hidden;
            this.drawSkeleton.SkeletonDataList.Clear();
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            if(txbFileName.Text != "" && txbFileName.Text.Contains(" ") == false)
            {
                this.drawSkeleton.WriteToFile(txbFileName.Text);
                this.files.Clear();
                this.files = this.drawSkeleton.ReadFiles();
                lvwLibrary.ItemsSource = null;
                lvwLibrary.ItemsSource = this.files;
                grdPopup.Visibility = Visibility.Hidden;
            }

            else
            {
                MessageBox.Show("Gelieve een correcte titel mee te geven");
            }

        }

        
        
    }
    }

