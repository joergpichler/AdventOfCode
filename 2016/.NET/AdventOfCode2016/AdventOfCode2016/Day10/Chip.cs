namespace AdventOfCode2016.Day10;

public class Chip
{
    public Chip(int value)
    {
        Value = value;
    }

    public ChipOwner? Owner { get; set; }

    public int Value { get; }
}