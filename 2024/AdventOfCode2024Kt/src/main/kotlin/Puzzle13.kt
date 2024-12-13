package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle13 : Puzzle<List<ClawMachine>, Long>(13, 2024) {
    override fun getTestData(): String {
        return "Button A: X+94, Y+34\n" +
                "Button B: X+22, Y+67\n" +
                "Prize: X=8400, Y=5400\n" +
                "\n" +
                "Button A: X+26, Y+66\n" +
                "Button B: X+67, Y+21\n" +
                "Prize: X=12748, Y=12176\n" +
                "\n" +
                "Button A: X+17, Y+86\n" +
                "Button B: X+84, Y+37\n" +
                "Prize: X=7870, Y=6450\n" +
                "\n" +
                "Button A: X+69, Y+23\n" +
                "Button B: X+27, Y+71\n" +
                "Prize: X=18641, Y=10279"
    }

    override fun parse(input: String): List<ClawMachine> {
        val lines = input.lines()
        val clawMachines = mutableListOf<ClawMachine>()

        for (i in lines.indices step 4) {
            val buttonALine = lines[i]
            val buttonBLine = lines[i + 1]
            val prizeLine = lines[i + 2]

            val a = parseVector(buttonALine)
            val b = parseVector(buttonBLine)
            val prize = parsePoint(prizeLine)

            clawMachines.add(ClawMachine(a, b, prize))
        }

        return clawMachines
    }

    private fun parseVector(line: String): Pair<Long, Long> {
        val parts = line.split(", ")
        val x = parts[0].substringAfter("X+").toLong()
        val y = parts[1].substringAfter("Y+").toLong()
        return Pair(x, y)
    }

    private fun parsePoint(line: String): Pair<Long, Long> {
        val parts = line.split(", ")
        val x = parts[0].substringAfter("X=").toLong()
        val y = parts[1].substringAfter("Y=").toLong()
        return Pair(x, y)
    }

    override fun solvePart02(input: List<ClawMachine>): Long {
        var result: Long = 0
        for (clawMachine in input.map {
            ClawMachine(
                it.a,
                it.b,
                Pair(it.prize.first + 10000000000000, it.prize.second + 10000000000000)
            )
        }) {
            val (a, b, prize) = clawMachine
            val solution = solveDiophantine(a, b, prize)
            if (solution != null) {
                val (n, m) = solution
                result += n * 3 + m
            }
        }
        return result
    }

    override fun solvePart01(input: List<ClawMachine>): Long {
        var result: Long = 0
        for (clawMachine in input) {
            val (a, b, prize) = clawMachine
            val solution = solveDiophantine(a, b, prize)
            if (solution != null) {
                val (n, m) = solution
                result += n * 3 + m
            }
        }
        return result
    }

    fun solveDiophantine(a: Pair<Long, Long>, b: Pair<Long, Long>, x: Pair<Long, Long>): Pair<Long, Long>? {
        val (a1, a2) = a
        val (b1, b2) = b
        val (x1, x2) = x

        // Solve for n and m using integer arithmetic
        // Step 1: Use the determinant of the matrix to check consistency
        val det: Long = a1 * b2 - a2 * b1
        if (det == 0L) {
            println("No unique solution exists, determinant is zero.")
            return null
        }

        // Step 2: Use Cramer's rule to find a general solution
        val n = (x1 * b2 - x2 * b1) / det
        val m = (a1 * x2 - a2 * x1) / det

        // Step 3: Verify integer solution
        if ((x1 == n * a1 + m * b1) && (x2 == n * a2 + m * b2)) {
            return Pair(n, m)
        }

//        println("No integer solution exists.")
        return null
    }
}

data class ClawMachine(val a: Pair<Long, Long>, val b: Pair<Long, Long>, val prize: Pair<Long, Long>)