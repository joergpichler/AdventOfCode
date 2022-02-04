namespace AdventOfCode2016.Day10;

public class ChipFactory
{
    private readonly IDictionary<int, Chip> _chips = new Dictionary<int, Chip>();

    public Chip GetChip(int value)
    {
        if (_chips.ContainsKey(value))
        {
            throw new InvalidOperationException($"Chip with value {value} has already been manufactured");
        }

        var chip = new Chip(value);
        _chips.Add(chip.Value, chip);

        return chip;
    }
}