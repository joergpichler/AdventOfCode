using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Combinatorics.Collections;

namespace Day24
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var numbers = File.ReadAllLines("input.txt").Select(x => int.Parse(x)).ToList();

            Console.WriteLine($"{CalcMinQte(numbers, 3)}");
            Console.WriteLine($"{CalcMinQte(numbers, 4)}");
        }

        static long CalcMinQte(IList<int> numbers, int targetSum, int depth, int targetDepth)
        {
            if (depth == targetDepth)
            {
                return 0;
            }

            for (var i = 1; i < numbers.Count; i++)
            {
                foreach (var c in new Combinations<int>(numbers, i, GenerateOption.WithoutRepetition).Where(x => x.Sum() == targetSum))
                {
                    var remainingNumbers = numbers.Except(c).ToList();
                    if (CalcMinQte(remainingNumbers, targetSum, depth + 1, targetDepth) != -1)
                    {
                        var result = c.Select(x => (long) x).Aggregate((a, b) => a * b);
                        return result;
                    }
                }
            }

            return -1;
        }

        static long CalcMinQte(IList<int> numbers, int parts)
        {
            var sum = numbers.Sum() / parts;

            if ((double)sum != (double)numbers.Sum() / parts)
            {
                throw new InvalidOperationException();
            }

            return CalcMinQte(numbers, sum, 1, parts);
        }
    }
}
