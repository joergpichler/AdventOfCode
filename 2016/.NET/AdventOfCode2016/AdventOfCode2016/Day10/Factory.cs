using System.Text.RegularExpressions;

namespace AdventOfCode2016.Day10;

public class Factory
{
    private readonly ChipFactory _chipFactory = new();
    private readonly BotFactory _botFactory = new();
    private readonly IDictionary<int, Bin> _bins = new Dictionary<int, Bin>();

    public void Run(IEnumerable<string> instructions)
    {
        var instructionList = instructions.ToList();

        RunInitializationInstructions(instructionList);
        RunWorkInstructions(instructionList);
    }

    private void RunWorkInstructions(List<string> instructionList)
    {
        var instructionRegex = new Regex(@"bot (\d+) gives low to ([a-z]+) (\d+) and high to ([a-z]+) (\d+)");

        while (instructionList.Count > 0)
        {
            for (int i = instructionList.Count - 1; i >= 0; i--)
            {
                var instruction = instructionList[i];
                var match = instructionRegex.Match(instruction);
                if (!match.Success)
                {
                    throw new InvalidOperationException($"Unknown instruction: {instruction}");
                }

                var sourceBot = _botFactory.GetBot(int.Parse(match.Groups[1].Value));

                if (!sourceBot.CanRemove())
                {
                    continue;
                }

                var lowTarget = match.Groups[2].Value;
                var lowTargetNumber = int.Parse(match.Groups[3].Value);
                var highTarget = match.Groups[4].Value;
                var highTargetNumber = int.Parse(match.Groups[5].Value);

                ChipOwner lowReceiver = lowTarget == "output" ? GetOutput(lowTargetNumber) :
                    lowTarget == "bot" ? _botFactory.GetBot(lowTargetNumber) : throw new InvalidOperationException();
                if (!lowReceiver.CanReceive())
                {
                    continue;
                }
                ChipOwner highReceiver = highTarget == "output" ? GetOutput(highTargetNumber) :
                    highTarget == "bot" ? _botFactory.GetBot(highTargetNumber) : throw new InvalidOperationException();
                if (!highReceiver.CanReceive())
                {
                    continue;
                }

                var chips = sourceBot.GetChips();
                
                lowReceiver.ReceiveChip(sourceBot.RemoveChip(chips.lowChip));
                highReceiver.ReceiveChip(sourceBot.RemoveChip(chips.highChip));

                instructionList.RemoveAt(i);
            }
        }
    }

    private ChipOwner GetOutput(int number)
    {
        if (!_bins.TryGetValue(number, out var bin))
        {
            bin = new Bin(number);
            _bins.Add(bin.Number, bin);
        }

        return bin;
    }

    private void RunInitializationInstructions(List<string> instructionList)
    {
        var initRegex = new Regex(@"value (\d+) goes to bot (\d+)");

        for (int i = instructionList.Count - 1; i >= 0; i--)
        {
            var instruction = instructionList[i];
            var match = initRegex.Match(instruction);
            if (match.Success)
            {
                var chip = _chipFactory.GetChip(int.Parse(match.Groups[1].Value));
                var bot = _botFactory.GetBot(int.Parse(match.Groups[2].Value));
                bot.ReceiveChip(chip);
                instructionList.RemoveAt(i);
            }
        }
    }

    public Bot GetBot(int lowValue, int highValue)
    {
        return _botFactory.GetBots().First(b =>
            b.ComparedChips.HasValue && b.ComparedChips.Value.lowValue == lowValue && b.ComparedChips.Value.highValue == highValue);
    }

    public Bin GetBin(int number)
    {
        return _bins[number];
    }
}