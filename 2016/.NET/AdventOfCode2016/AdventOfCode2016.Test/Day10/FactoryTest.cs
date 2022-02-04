using AdventOfCode2016.Day10;
using NUnit.Framework;

namespace AdventOfCode2016.Test.Day10;

public class FactoryTest
{
    [Test]
    public void Test()
    {
        var instructions = File.ReadAllLines(@"Day10\Test.txt");
        var factory = new Factory();
        factory.Run(instructions);
        var bot = factory.GetBot(2, 5);

        Assert.That(bot.Number, Is.EqualTo(2));
    }

    [Test]
    public void Pt1()
    {
        var instructions = File.ReadAllLines(@"Day10\Input.txt");
        var factory = new Factory();
        factory.Run(instructions);
        var bot = factory.GetBot(17, 61);

        Assert.That(bot.Number, Is.EqualTo(113));
    }

    [Test]
    public void Pt2()
    {
        var instructions = File.ReadAllLines(@"Day10\Input.txt");
        var factory = new Factory();
        factory.Run(instructions);

        var bin0 = factory.GetBin(0);
        var bin1 = factory.GetBin(1);
        var bin2 = factory.GetBin(2);

        var result = bin0.GetChips().Single().Value * bin1.GetChips().Single().Value * bin2.GetChips().Single().Value;

        Assert.That(result, Is.EqualTo(12803));
    }
}