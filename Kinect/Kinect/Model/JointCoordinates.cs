using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect.Model
{
    public class JointCoordinates
    {
        [JsonProperty("jointname")]
        public String JointName { get; set; }
        [JsonProperty("coordinates")]
        public List<float> Coordinates { get; set; }
        //[JsonProperty("x")]
        //public float XCoordinate { get; set; }
        //[JsonProperty("y")]
        //public float YCoordinate { get; set; }
        //[JsonProperty("z")]
        //public float ZCoordinate { get; set; }
    }
}
