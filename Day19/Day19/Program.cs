using MathNet.Numerics.LinearAlgebra;

var scanners = Scanner.Parse("input.txt");

var baseScanner = scanners[0];
baseScanner.RelativeOrigin = Vector<double>.Build.Dense(3, 0.0);
var unassignedScanners = scanners.Skip(1).ToList();

while (unassignedScanners.Count > 0)
{
    Scanner? matchedScanner = null;

    foreach (var scanner in unassignedScanners)
    {
        if (ScannerMatcher.Matches(baseScanner, scanner))
        {
            matchedScanner = scanner;
            break;
        }
    }

    if (matchedScanner == null)
    {
        throw new Exception("No more matching scanner found?!");
    }

    ScannerMatcher.Match(baseScanner, matchedScanner);

    unassignedScanners.Remove(matchedScanner);
}

Console.WriteLine($"{baseScanner.Beacons.Count}");

var distances = new List<int>();
for (var i = 0; i < scanners.Count - 1; i++)
{
    for (var j = i + 1; j < scanners.Count; j++)
    {
        var distance = scanners[i].RelativeOrigin.Add(scanners[j].RelativeOrigin.Multiply(-1)).L1Norm();
        distances.Add((int) distance);
    }
}

Console.WriteLine($"{distances.Max()}");