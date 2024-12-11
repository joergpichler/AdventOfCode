package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle11 : Puzzle<List<Long>, Long>(11, 2024) {
    override fun getTestData(): String {
        return "125 17"
    }

    override fun parse(input: String): List<Long> {
        return input.split(" ").map { it.toLong() }
    }

    override fun solvePart02(input: List<Long>): Long {
        return solve(input, 75)
    }

    override fun solvePart01(input: List<Long>): Long {
        return solve(input, 25)
    }

    fun solve(input: List<Long>, loops: Int): Long {
        var result: Long = 0L
        for (number in input) {
            result += countNumbers(number, 0, loops)
        }
        return result
    }

    fun countNumbers(number: Long, depth: Int, targetDepth: Int): Long {
        val key = CacheKey(number, depth, targetDepth)
        if (cache.containsKey(key)) {
            return cache[key]!!
        }

        if (depth == targetDepth) {
            return 1
        }

        if (number == 0L) {
            val result = countNumbers(1L, depth + 1, targetDepth)
            cache[key] = result
            return result
        }

        if (number.toString().length % 2 == 0) {
            val str = number.toString()
            val firstHalf = str.substring(0, str.length / 2).toLong()
            val secondHalf = str.substring(str.length / 2).toLong()
            val firstHalfResult = countNumbers(firstHalf, depth + 1, targetDepth)
            cache[CacheKey(firstHalf, depth + 1, targetDepth)] = firstHalfResult
            val secondHalfResult = countNumbers(secondHalf, depth + 1, targetDepth)
            cache[CacheKey(secondHalf, depth + 1, targetDepth)] = secondHalfResult
            return firstHalfResult + secondHalfResult
        }

        val newNumber = number * 2024
        val result = countNumbers(newNumber, depth + 1, targetDepth)
        cache[CacheKey(newNumber, depth + 1, targetDepth)] = result
        return result
    }

        private val cache = mutableMapOf<CacheKey, Long>()

        data class CacheKey(val number: Long, val depth: Int, val targetDepth: Int)
    }