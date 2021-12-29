using System.Diagnostics;
using System.Reflection;
using MathNet.Numerics.LinearAlgebra;

var scanners = ReadInput("input.txt");

var baseScanner = scanners[0];
baseScanner.RelativeOrigin = Vector<double>.Build.Dense(3, 0.0);
var unassigendScanners = scanners.Skip(1).ToList();

while (unassigendScanners.Count > 0)
{
    Scanner? matchedScanner = null;

    foreach (var scanner in unassigendScanners)
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

    unassigendScanners.Remove(matchedScanner);
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

IList<Scanner> ReadInput(string filename)
{
    using var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream($"Day19.{filename}");
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

    public Vector<double> RelativeOrigin { get; set; }
}

[DebuggerDisplay("{Name}: {X},{Y},{Z}")]
class Beacon
{
    public Beacon(string name, int x, int y, int z)
    {
        Name = name;
        X = x;
        Y = y;
        Z = z;
    }

    public string Name { get; }

    public int X { get; }

    public int Y { get; }

    public int Z { get; }

    protected bool Equals(Beacon other)
    {
        return X == other.X && Y == other.Y && Z == other.Z;
    }

    public override bool Equals(object? obj)
    {
        if (ReferenceEquals(null, obj)) return false;
        if (ReferenceEquals(this, obj)) return true;
        if (obj.GetType() != this.GetType()) return false;
        return Equals((Beacon) obj);
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(X, Y, Z);
    }
}

[DebuggerDisplay("{BeaconA.Name}->{BeaconB.Name}: {Distance}")]
class BeaconDistance
{
    public BeaconDistance(Beacon beaconA, Beacon beaconB)
    {
        if (beaconA == beaconB)
        {
            throw new ArgumentException();
        }

        BeaconA = beaconA;
        BeaconB = beaconB;

        var dx = BeaconB.X - BeaconA.X;
        var dy = BeaconB.Y - BeaconA.Y;
        var dz = BeaconB.Z - BeaconA.Z;

        Vector = Vector<double>.Build.DenseOfArray(new double[] {dx, dy, dz});
    }

    public Beacon BeaconA { get; }

    public Beacon BeaconB { get; }

    public Vector<double> Vector { get; }

    public double Distance => Vector.L2Norm();

    protected bool Equals(BeaconDistance other)
    {
        return BeaconA.Equals(other.BeaconA) && BeaconB.Equals(other.BeaconB) ||
               BeaconA.Equals(other.BeaconB) && BeaconB.Equals(other.BeaconA);
    }

    public override bool Equals(object? obj)
    {
        if (ReferenceEquals(null, obj)) return false;
        if (ReferenceEquals(this, obj)) return true;
        if (obj.GetType() != this.GetType()) return false;
        return Equals((BeaconDistance) obj);
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(BeaconA, BeaconB);
    }

    public BeaconDistance Invert()
    {
        return new BeaconDistance(BeaconB, BeaconA);
    }
}

static class ScannerMatcher
{
    public static bool Matches(Scanner baseScanner, Scanner scanner)
    {
        // To match at least 12 points in 2 systems at least 66 (11 + 10 + 9 + ...) distances must match
        var matchingDistancesCount = baseScanner.BeaconDistances.Select(x => x.Distance)
            .Intersect(scanner.BeaconDistances.Select(x => x.Distance))
            .Count();
        return matchingDistancesCount >= 10;
    }

    public static void Match(Scanner baseScanner, Scanner scanner)
    {
        if (!Matches(baseScanner, scanner))
        {
            throw new Exception("Scanners do not match");
        }

        var baseDistances = baseScanner.BeaconDistances.GroupBy(x => x.Distance).ToDictionary(x => x.Key, x => x.First());

        List<(BeaconDistance baseDistances, BeaconDistance targetDistance)> distanceMatches = new();

        foreach (var beaconDistance in scanner.BeaconDistances)
        {
            if (!baseDistances.TryGetValue(beaconDistance.Distance, out var baseDistance))
            {
                continue;
            }

            distanceMatches.Add((baseDistance, beaconDistance));
        }

        var (transformationMatrix, translationVector) = FindTransformation(distanceMatches);
        scanner.RelativeOrigin = translationVector;

        Console.WriteLine($"Scanner {scanner.Number}: {(int)translationVector[0]},{(int)translationVector[1]},{(int)translationVector[2]}");

        foreach (var transformedBeacon in scanner.Beacons.Select(x => x.Transform(transformationMatrix, translationVector)))
        {
            if (baseScanner.Beacons.Contains(transformedBeacon))
            {
                continue;
            }

            baseScanner.AddBeacon(transformedBeacon);
        }
    }

    private static (Matrix<double> transformationMatrix, Vector<double> translationVector) FindTransformation(
        List<(BeaconDistance baseDistance, BeaconDistance targetDistance)> distanceMatches)
    {
        Matrix<double> foundTransformation = null;

        int ctr = 0;
        while (foundTransformation == null && ctr < distanceMatches.Count)
        {
            foreach (var transformationMatrix in TransformationMatrices.Get())
            {
                var baseDistance = distanceMatches[ctr].baseDistance;
                var transformedTarget = distanceMatches[ctr].targetDistance.Transform(transformationMatrix);

                if (baseDistance.Vector.Equals(transformedTarget.Vector))
                {
                    foundTransformation = transformationMatrix;
                    break;
                }

                if (baseDistance.Vector.Equals(transformedTarget.Vector.Invert()))
                {
                    foundTransformation = transformationMatrix;
                    break;
                }
            }

            ctr++;
        }
        
        if (foundTransformation == null)
        {
            throw new Exception("No transformation matrix found");
        }

        distanceMatches = distanceMatches.Select(x =>
            (baseDistance: x.baseDistance, targetDistance: x.targetDistance.Transform(foundTransformation))).Select(x =>
        {
            if (x.baseDistance.Vector.Equals(x.targetDistance.Vector))
            {
                return (baseDistance: x.baseDistance, targetDistance: x.targetDistance);
            }

            return (baseDistance: x.baseDistance, targetDistance: x.targetDistance.Invert());
        }).ToList();

        if (!distanceMatches.All(x => x.baseDistance.Vector.Equals(x.targetDistance.Vector)))
        {
            var invalidMatches = distanceMatches.Where(x => !x.baseDistance.Vector.Equals(x.targetDistance.Vector)).ToList();
            foreach (var invalidMatch in invalidMatches)
            {
                distanceMatches.Remove(invalidMatch);
            }
        }

        var translation = Vector<double>.Build.Dense(new double[]
        {
            distanceMatches[0].baseDistance.BeaconA.X - distanceMatches[0].targetDistance.BeaconA.X,
            distanceMatches[0].baseDistance.BeaconA.Y - distanceMatches[0].targetDistance.BeaconA.Y,
            distanceMatches[0].baseDistance.BeaconA.Z - distanceMatches[0].targetDistance.BeaconA.Z
        });

        distanceMatches = distanceMatches.Select(x =>
            (baseDistance: x.baseDistance, targetDistance: x.targetDistance.Translate(translation))).ToList();

        if (!distanceMatches.All(x => x.baseDistance.BeaconA.ToVector().Equals(x.targetDistance.BeaconA.ToVector()) &&
                                      x.baseDistance.BeaconB.ToVector().Equals(x.targetDistance.BeaconB.ToVector())))
        {
            throw new Exception("Something went wrong");
        }

        return (foundTransformation, translation);
    }
}

static class TransformationMatrices
{
    private static readonly List<Matrix<double>> Matrices = new();

    public static IList<Matrix<double>> Get() => Matrices;

    static TransformationMatrices()
    {
        for (var sX = 0; sX < 2; sX++)
        {
            for (var sY = 0; sY < 2; sY++)
            {
                for (var sZ = 0; sZ < 2; sZ++)
                {
                    for (var iX = 0; iX < 3; iX++)
                    {
                        for (var iY = 0; iY < 3; iY++)
                        {
                            for (var iZ = 0; iZ < 3; iZ++)
                            {
                                if (iX == iY)
                                {
                                    continue;
                                }

                                if (iX == iZ)
                                {
                                    continue;
                                }

                                if (iY == iZ)
                                {
                                    continue;
                                }

                                var m = Matrix<double>.Build.Dense(3, 3);
                                m[iX, 0] = sX == 0 ? 1 : -1;
                                m[iY, 1] = sY == 0 ? 1 : -1;
                                m[iZ, 2] = sZ == 0 ? 1 : -1;

                                var det = m.Determinant();

                                if (m.Column(0).Count(x => x != 0) != 1 ||
                                    m.Column(1).Count(x => x != 0) != 1 ||
                                    m.Column(2).Count(x => x != 0) != 1)
                                {
                                    throw new Exception();
                                }

                                if (det == 1)
                                {
                                    Matrices.Add(m);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

static class Extensions
{
    public static Vector<double> ToVector(this Beacon b)
    {
        return Vector<double>.Build.DenseOfArray(new double[] {b.X, b.Y, b.Z});
    }

    public static Beacon Transform(this Beacon b, Matrix<double> transformationMatrix)
    {
        var vector = b.ToVector();
        var transformedVector = transformationMatrix.Multiply(vector);
        return new Beacon(b.Name, (int) transformedVector[0], (int) transformedVector[1], (int) transformedVector[2]);
    }

    public static BeaconDistance Transform(this BeaconDistance bd, Matrix<double> transformationMatrix)
    {
        return new BeaconDistance(bd.BeaconA.Transform(transformationMatrix),
            bd.BeaconB.Transform(transformationMatrix));
    }

    public static Vector<double> Invert(this Vector<double> v)
    {
        return Vector<double>.Build.Dense(new[] {-v[0], -v[1], -v[2]});
    }

    public static BeaconDistance Translate(this BeaconDistance bd, Vector<double> v)
    {
        return new BeaconDistance(bd.BeaconA.Translate(v), bd.BeaconB.Translate(v));
    }

    public static Beacon Translate(this Beacon b, Vector<double> v)
    {
        return new Beacon(b.Name, b.X + (int) v[0], b.Y + (int) v[1], b.Z + (int) v[2]);
    }

    public static Beacon Transform(this Beacon b, Matrix<double> transformationMatrix, Vector<double> translationVector)
    {
        var transformedVector = transformationMatrix.Multiply(b.ToVector()).Add(translationVector);
        return new Beacon(b.Name, (int) transformedVector[0], (int) transformedVector[1], (int) transformedVector[2]);
    }
}