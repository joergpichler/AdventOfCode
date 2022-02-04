namespace AdventOfCode2016.Day10;

public class Bin : ChipOwner
{
    public Bin(int number)
    {
        Number = number;
    }

    public int Number { get; }

    public IEnumerable<Chip> GetChips() => Chips;
}