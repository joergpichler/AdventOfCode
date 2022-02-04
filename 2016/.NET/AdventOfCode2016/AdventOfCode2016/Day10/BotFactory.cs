namespace AdventOfCode2016.Day10;

public class BotFactory
{
    private readonly IDictionary<int, Bot> _bots = new Dictionary<int, Bot>();

    public Bot GetBot(int number)
    {
        if (!_bots.TryGetValue(number, out var bot))
        {
            bot = new Bot(number);
            _bots.Add(bot.Number, bot);
        }

        return bot;
    }

    public IEnumerable<Bot> GetBots() => _bots.Values;
}