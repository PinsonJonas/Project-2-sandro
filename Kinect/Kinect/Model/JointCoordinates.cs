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
        
    }
}
