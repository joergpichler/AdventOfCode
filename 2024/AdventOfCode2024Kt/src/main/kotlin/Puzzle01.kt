package de.pichlerj

import de.pichlerj.base.Puzzle
import kotlin.math.abs

class Puzzle01 : Puzzle<Pair<List<Int>, List<Int>>, Int>(1, 2024) {
    override fun getTestData(): String {
        return "3   4\n" +
                "4   3\n" +
                "2   5\n" +
                "1   3\n" +
                "3   9\n" +
                "3   3"
    }

    override fun parse(input: String): Pair<List<Int>, List<Int>> {
        val leftList = mutableListOf<Int>()
        val rightList = mutableListOf<Int>()
        input.lines().forEach {
            // use regex to detect two numbers split by whitespaces
            val regex = Regex("""\s+""")
            val split = it.split(regex)
            leftList.add(split[0].toInt())
            rightList.add(split[1].toInt())
        }
        return Pair(leftList, rightList)
    }

    override fun solvePart02(input: Pair<List<Int>, List<Int>>): Int {
        val rightList = input.second
        val rightListDict = mutableMapOf<Int, Int>()
        rightList.forEach {
            rightListDict[it] = rightListDict.getOrDefault(it, 0) + 1
        }

        var sum = 0
        val leftList = input.first
        leftList.forEach {
            val timesInRightList = rightListDict.getOrDefault(it, 0)
            sum += it * timesInRightList
        }

        return sum
    }

    override fun solvePart01(input: Pair<List<Int>, List<Int>>): Int {
        val sortedLeftList = input.first.sorted()
        val sortedRightList = input.second.sorted()

        var sum = 0
        for(i in sortedLeftList.indices){
            val left = sortedLeftList[i]
            val right = sortedRightList[i]
            val abs = abs(left - right)
            sum += abs
        }

        return sum
    }
}