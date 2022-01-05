using MathNet.Numerics.LinearAlgebra;

static class ScannerMatcher
{
    public static bool Matches(Scanner baseScanner, Scanner scanner)
    {
        // To match at least 12 points in 2 systems at least 66 (11 + 10 + 9 + ...) distances must match
        var matchingDistancesCount = baseScanner.BeaconDistances.Select(x => x.Id)
            .Intersect(scanner.BeaconDistances.Select(x => x.Id))
            .Count();
        return matchingDistancesCount >= 66;
    }

    public static void Match(Scanner baseScanner, Scanner scanner)
    {
        if (!Matches(baseScanner, scanner))
        {
            throw new Exception("Scanners do not match");
        }

        var baseDistances = baseScanner.BeaconDistances.GroupBy(x => x.Id).ToDictionary(x => x.Key, x => x.ToList());

        List<(BeaconDistance baseDistances, BeaconDistance targetDistance)> distanceMatches = new();

        foreach (var beaconDistance in scanner.BeaconDistances)
        {
            if (!baseDistances.TryGetValue(beaconDistance.Id, out var baseDistanceMatches))
            {
                continue;
            }

            var baseDistance = baseDistanceMatches.First();
            if (baseDistanceMatches.Count > 1)
            {
                throw new Exception();
            }

            distanceMatches.Add((baseDistance, beaconDistance));
        }

        var (transformationMatrix, translationVector) = FindTransformation(distanceMatches);
        scanner.RelativeOrigin = translationVector;

        Console.WriteLine(
            $"Scanner {scanner.Number}: {(int) translationVector[0]},{(int) translationVector[1]},{(int) translationVector[2]}");

        foreach (var transformedBeacon in scanner.Beacons.Select(x =>
                     x.Transform(transformationMatrix, translationVector)))
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
        Matrix<double>? foundTransformation = null;

        foreach (var transformationMatrix in Matrices.TransformationMatrices)
        {
            var baseDistance = distanceMatches[0].baseDistance;
            var transformedTarget = distanceMatches[0].targetDistance.Transform(transformationMatrix);

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

        if (foundTransformation == null)
        {
            throw new Exception("No transformation matrix found");
        }

        distanceMatches = distanceMatches.Select(x =>
            (x.baseDistance, targetDistance: x.targetDistance.Transform(foundTransformation))).Select(x =>
        {
            if (x.baseDistance.Vector.Equals(x.targetDistance.Vector))
            {
                return (x.baseDistance, x.targetDistance);
            }

            return (x.baseDistance, targetDistance: x.targetDistance.Invert());
        }).ToList();

        if (!distanceMatches.All(x => x.baseDistance.Vector.Equals(x.targetDistance.Vector)))
        {
            throw new Exception();
        }

        var translationVector = Vector<double>.Build.Dense(new double[]
        {
            distanceMatches[0].baseDistance.BeaconA.X - distanceMatches[0].targetDistance.BeaconA.X,
            distanceMatches[0].baseDistance.BeaconA.Y - distanceMatches[0].targetDistance.BeaconA.Y,
            distanceMatches[0].baseDistance.BeaconA.Z - distanceMatches[0].targetDistance.BeaconA.Z
        });

        distanceMatches = distanceMatches.Select(x =>
            (x.baseDistance, targetDistance: x.targetDistance.Transform(translationVector: translationVector))).ToList();

        if (!distanceMatches.All(x => x.baseDistance.BeaconA.ToVector().Equals(x.targetDistance.BeaconA.ToVector()) &&
                                      x.baseDistance.BeaconB.ToVector().Equals(x.targetDistance.BeaconB.ToVector())))
        {
            throw new Exception("Something went wrong");
        }

        return (foundTransformation, translationVector);
    }
}