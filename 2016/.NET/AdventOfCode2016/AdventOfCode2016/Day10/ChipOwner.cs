using System.ComponentModel;

namespace AdventOfCode2016.Day10;

public abstract class ChipOwner
{
    protected readonly IList<Chip> Chips = new List<Chip>();

    public virtual void ReceiveChip(Chip chip)
    {
        if (chip.Owner == this)
        {
            throw new InvalidAsynchronousStateException("Chip already owned");
        }

        chip.Owner = this;
        Chips.Add(chip);
    }

    public virtual Chip RemoveChip(Chip chip)
    {
        if (!Chips.Contains(chip))
        {
            throw new InvalidOperationException("Chip does not belong to this owner");
        }

        chip.Owner = null;
        Chips.Remove(chip);

        return chip;
    }

    public virtual bool CanReceive() => true;
}