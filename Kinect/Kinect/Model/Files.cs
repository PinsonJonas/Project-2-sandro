using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kinect.Model
{
    public class Files
    {
        public string Name { get; set; }
        public string Content { get; set; }

        public override string ToString()
        {
            return Name;
        }
    }
}
