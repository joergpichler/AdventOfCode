using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace Day23
{
    public static class AssemblyExtensions
    {
        public static IEnumerable<string> GetEmbeddedResourceLines(this Assembly assembly, string resourceName)
        {
            using (var stream = assembly.GetManifestResourceStream("Day23." + resourceName))
            {
                using (var reader = new StreamReader(stream))
                {
                    string line;
                    while ((line = reader.ReadLine()) != null)
                    {
                        yield return line;
                    }
                }
            }
        }
    }
}