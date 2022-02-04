namespace AdventOfCode2016.Day10;

public class Bot : ChipOwner
{
    public Bot(int number)
    {
        Number = number;
    }

    public int Number { get; }

    public override void ReceiveChip(Chip chip)
    {
        if (Chips.Count >= 2)
        {
            throw new InvalidOperationException("Bot can only hold 2 chips");
        }

        base.ReceiveChip(chip);
    }

    public override bool CanReceive() => Chips.Count < 2;

    public bool CanRemove() => Chips.Count == 2;

    public (Chip lowChip, Chip highChip) GetChips()
    {
        if (Chips.Count != 2)
        {
            throw new InvalidOperationException();
        }

        Chip lowChip;
        Chip highChip;

        if (Chips[0].Value > Chips[1].Value)
        {
            lowChip = Chips[1];
            highChip = Chips[0];
        }
        else
        {
            lowChip = Chips[0];
            highChip = Chips[1];
        }

        ComparedChips = (lowChip.Value, highChip.Value);
        return (lowChip, highChip);
    }

    public (int lowValue, int highValue)? ComparedChips { get; private set; }
}