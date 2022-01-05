using System.Diagnostics;
using MathNet.Numerics.LinearAlgebra;

[DebuggerDisplay("{BeaconA.Name}->{BeaconB.Name}: {Id}")]
class BeaconDistance
{
    public BeaconDistance(Beacon beaconA, Beacon beaconB)
    {
        if (beaconA.Equals(beaconB))
        {
            throw new ArgumentException();
        }

        BeaconA = beaconA;
        BeaconB = beaconB;

        var dx = BeaconB.X - BeaconA.X;
        var dy = BeaconB.Y - BeaconA.Y;
        var dz = BeaconB.Z - BeaconA.Z;

        Vector = Vector<double>.Build.DenseOfArray(new double[] {dx, dy, dz});

        Id = string.Join('-', new[] {dx, dy, dz}.Select(Math.Abs).OrderBy(x => x).Select(x => x.ToString()));
    }

    public string Id { get; }

    public Beacon BeaconA { get; }

    public Beacon BeaconB { get; }

    public Vector<double> Vector { get; }

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