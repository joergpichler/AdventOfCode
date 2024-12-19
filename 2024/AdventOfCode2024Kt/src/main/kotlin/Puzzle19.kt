package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle19 : Puzzle<Puzzle19Data, Long>(19, 2024) {
    override fun getTestData(): String {
        return "r, wr, b, g, bwu, rb, gb, br\n" +
                "\n" +
                "brwrr\n" +
                "bggr\n" +
                "gbbr\n" +
                "rrbgbr\n" +
                "ubwu\n" +
                "bwurrg\n" +
                "brgr\n" +
                "bbrgwb"
    }

    override fun parse(input: String): Puzzle19Data {
        val lines = input.lines()
        val words = lines[0].split(", ")
        val targets = lines.subList(2, lines.size)
        return Puzzle19Data(words, targets)
    }

    override fun solvePart02(input: Puzzle19Data): Long {
        return _results!!.sumOf { it }
    }

    private var _results: List<Long>? = null

    override fun solvePart01(input: Puzzle19Data): Long {
        _cache.clear()
        _results = input.targets.map {
            countConstruct(it, input.words)
        }
        return _results!!.count { it > 0 }.toLong()
    }

    private val _cache = mutableMapOf<String, Long>()

    private fun countConstruct(target: String, words: List<String>): Long {
        if (_cache.containsKey(target)) {
            return _cache[target]!!
        }

        if (target.isEmpty()) {
            return 1
        }

        var result = 0L

        for (word in words) {
            if (target.length >= word.length && target.startsWith(word)) {
                val suffix = target.substring(word.length)
                result += countConstruct(suffix, words)
            }
        }

        _cache[target] = result
        return result
    }

}

data class Puzzle19Data(val words: List<String>, val targets: List<String>)