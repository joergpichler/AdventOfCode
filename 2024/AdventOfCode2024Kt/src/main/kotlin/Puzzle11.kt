package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle11 : Puzzle<List<Long>, Int>(11, 2024) {
    override fun getTestData(): String {
        return "125 17"
    }

    override fun parse(input: String): List<Long> {
        return input.split(" ").map { it.toLong() }
    }

    override fun solvePart02(input: List<Long>): Int {
        return solve(input, 75)
    }

    override fun solvePart01(input: List<Long>): Int {
        return solve(input, 25)
    }

    fun solve(input: List<Long>, loops: Int): Int {
        var list = input.toList()

        for (i in 0 until loops) {
            val transformedList = mutableListOf<Long>()
            for (num in list) {
                if (num == 0L) {
                    transformedList.add(1L)
                } else if (num.toString().length % 2 == 0) {
                    val str = num.toString()
                    val firstHalf = str.substring(0, str.length / 2).toLong()
                    val secondHalf = str.substring(str.length / 2).toLong()
                    transformedList.add(firstHalf)
                    transformedList.add(secondHalf)
                } else {
                    transformedList.add(num * 2024)
                }
            }
            list = transformedList
        }

        return list.size
    }
}