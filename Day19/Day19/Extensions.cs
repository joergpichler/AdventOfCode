using MathNet.Numerics.LinearAlgebra;

static class Extensions
{
    public static Vector<double> Invert(this Vector<double> v)
    {
        return Vector<double>.Build.Dense(new[] { -v[0], -v[1], -v[2] });
    }

    public static Vector<double> ToVector(this Beacon b)
    {
        return Vector<double>.Build.DenseOfArray(new double[] {b.X, b.Y, b.Z});
    }

    public static BeaconDistance Transform(this BeaconDistance bd, Matrix<double>? transformationMatrix = null, Vector<double>? translationVector = null)
    {
        return new BeaconDistance(bd.BeaconA.Transform(transformationMatrix, translationVector),
            bd.BeaconB.Transform(transformationMatrix, translationVector));
    }

    public static Beacon Transform(this Beacon b, Matrix<double>? transformationMatrix = null, Vector<double>? translationVector = null)
    {
        var transformedVector = transformationMatrix != null ? transformationMatrix.Multiply(b.ToVector()) : b.ToVector();
        if (translationVector != null)
        {
            transformedVector = transformedVector.Add(translationVector);
        }
        return new Beacon(b.Name, (int) transformedVector[0], (int) transformedVector[1], (int) transformedVector[2]);
    }
}