package de.pichlerj

import de.pichlerj.base.Puzzle
import kotlin.math.abs

class Puzzle02 : Puzzle<List<List<Int>>, Int>(2, 2024) {
    override fun getTestData(): String {
        return "7 6 4 2 1\n" +
                "1 2 7 8 9\n" +
                "9 7 6 2 1\n" +
                "1 3 2 4 5\n" +
                "8 6 4 4 1\n" +
                "1 3 6 7 9"
    }

    override fun parse(input: String): List<List<Int>> {
        return input.lines().map { l -> l.split(' ').map { n -> n.toInt() } }
    }

    override fun solvePart02(input: List<List<Int>>): Int {
        var result = 0
        for (report in input) {
            if (solvePart01(report.many()) > 0){
                result += 1
            }
        }
        return result
    }

    override fun solvePart01(input: List<List<Int>>): Int {
        return input.count { it ->
            val gradients = it.gradients()
            (gradients.isIncreasing() || gradients.isDecreasing()) && gradients.hasCorrectStepSize()
        }
    }
}

private fun List<Int>.hasCorrectStepSize(): Boolean {
    return this.map { abs(it) }.all { it in 1..3 }
}

private fun List<Int>.isDecreasing(): Boolean {
    return this.all { it < 0 }
}

private fun List<Int>.isIncreasing(): Boolean {
    return this.all { it > 0 }
}

private fun List<Int>.gradients(): List<Int> {
    return this.zipWithNext { a, b -> b - a }
}

private fun List<Int>.many(): List<List<Int>> {
    return List(this.size) { index ->
        this.filterIndexed { i, _ -> i != index }
    }
}