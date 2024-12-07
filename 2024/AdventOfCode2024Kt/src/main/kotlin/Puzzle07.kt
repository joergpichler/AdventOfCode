package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle07 : Puzzle<List<Puzzle07Data>, Long>(7, 2024) {
    override fun getTestData(): String {
        return "190: 10 19\n" +
                "3267: 81 40 27\n" +
                "83: 17 5\n" +
                "156: 15 6\n" +
                "7290: 6 8 6 15\n" +
                "161011: 16 10 13\n" +
                "192: 17 8 14\n" +
                "21037: 9 7 18 13\n" +
                "292: 11 6 16 20"
    }

    override fun parse(input: String): List<Puzzle07Data> {
        val data = mutableListOf<Puzzle07Data>()
        input.lines().forEach {
            val split1 = it.split(": ")
            val split2 = split1[1].split(" ")
            data.add(Puzzle07Data(split1[0].toLong(), split2.map { it.toLong() }))
        }
        return data
    }

    override fun solvePart01(input: List<Puzzle07Data>): Long {
        return input.filter { it.getNumOfSolutions(1) > 0 }.sumOf { it.result }
    }

    override fun solvePart02(input: List<Puzzle07Data>): Long {
        return input.filter { it.getNumOfSolutions(2) > 0 }.sumOf { it.result }
    }
}

class Puzzle07Data(val result: Long, val numbers: List<Long>) {
    fun getNumOfSolutions(part: Int): Int {
        val combinations = if(part == 1) generateCombinations(numbers.size - 1) else generateCombinations2(numbers.size - 1)
        var result = 0
        for (combination in combinations) {
            if (solve(combination)) {
                result += 1
            }
        }
        return result
    }

    private fun solve(combination: List<Int>): Boolean {
        var result = getOperation(combination[0])(numbers[0], numbers[1])

        for (i in 2 until numbers.size) {
            result = getOperation(combination[i - 1])(result, numbers[i])
        }

        return result == this.result
    }

    private fun generateCombinations(n: Int): List<List<Int>> {
        val combinations = mutableListOf<List<Int>>()
        val totalCombinations = 1 shl n // 2^N using bit shift

        for (i in 0 until totalCombinations) {
            val combination = mutableListOf<Int>()
            for (j in 0 until n) {
                // Check if the j-th bit in i is set (1) or not (0)
                combination.add((i shr j) and 1)
            }
            combinations.add(combination)
        }

        return combinations
    }

    private fun generateCombinations2(n: Int): List<List<Int>> {
        val combinations = mutableListOf<List<Int>>()
        val totalCombinations = Math.pow(3.0, n.toDouble()).toInt() // 3^N

        for (i in 0 until totalCombinations) {
            val combination = mutableListOf<Int>()
            var number = i
            for (j in 0 until n) {
                combination.add(number % 3) // Get the current digit in base 3
                number /= 3 // Move to the next digit
            }
            combinations.add(combination)
        }

        return combinations
    }

    private fun getOperation(index: Int): (Long, Long) -> Long {
        return when (index) {
            0 -> { a, b -> a + b }
            1 -> { a, b -> a * b }
            2 -> { a, b -> (a.toString() + b.toString()).toLong() }
            else -> throw IllegalArgumentException("Invalid operation index")
        }
    }


}