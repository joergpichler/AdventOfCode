using System.Diagnostics;

[DebuggerDisplay("{Name}: {X},{Y},{Z}")]
internal class Beacon
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