using System.Diagnostics;
using System.Reflection;
using MathNet.Numerics.LinearAlgebra;

[DebuggerDisplay("{Number}")]
class Scanner
{
    private readonly List<Beacon> _beacons = new();
    private readonly List<BeaconDistance> _beaconDistances = new();

    public Scanner(int number)
    {
        Number = number;
    }

    public int Number { get; }

    public IReadOnlyCollection<Beacon> Beacons => _beacons;

    public IReadOnlyCollection<BeaconDistance> BeaconDistances => _beaconDistances;

    public void AddBeacon(int x, int y, int z)
    {
        var beacon = new Beacon($"{Number}-{_beacons.Count + 1}", x, y, z);
        AddBeacon(beacon);
    }

    public void AddBeacon(Beacon beacon)
    {
        foreach (var existingBeacon in _beacons)
        {
            _beaconDistances.Add(new BeaconDistance(existingBeacon, beacon));
        }

        _beacons.Add(beacon);
    }

    public Vector<double>? RelativeOrigin { get; set; }

    public static IList<Scanner> Parse(string fileName)
    {
        using var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream($"Day19.{fileName}");
        using var streamReader = new StreamReader(stream);

        var scanners = new List<Scanner>();
        Scanner scanner = null;

        var line = streamReader.ReadLine();
        while (line != null)
        {
            if (line.StartsWith("---"))
            {
                if (scanner != null && !scanners.Contains(scanner))
                {
                    scanners.Add(scanner);
                }

                scanner = new Scanner(int.Parse(line.Trim('-').Trim().Split(' ')[1]));
            }
            else if (!string.IsNullOrWhiteSpace(line))
            {
                var points = line.Split(',').Select(int.Parse).ToArray();
                scanner.AddBeacon(points[0], points[1], points[2]);
            }

            line = streamReader.ReadLine();
        }

        if (scanner != null && !scanners.Contains(scanner))
        {
            scanners.Add(scanner);
        }

        return scanners;
    }
}