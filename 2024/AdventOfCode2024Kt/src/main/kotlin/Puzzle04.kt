package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle04 : Puzzle<List<String>, Int>(4, 2024) {
    override fun getTestData(): String {
        return "MMMSXXMASM\n" +
                "MSAMXMSMSA\n" +
                "AMXSXMAAMM\n" +
                "MSAMASMSMX\n" +
                "XMASAMXAMM\n" +
                "XXAMMXXAMA\n" +
                "SMSMSASXSS\n" +
                "SAXAMASAAA\n" +
                "MAMMMXMMMM\n" +
                "MXMXAXMASX"
    }

    override fun parse(input: String): List<String> {
        return input.split("\n")
    }

    override fun solvePart02(input: List<String>): Int {
        var result = 0
        for (row in input.indices) {
            for (col in input[row].indices) {
                if (isXmasX(input, row, col)) {
                    result += 1
                }
            }
        }

        return result
    }

    override fun solvePart01(input: List<String>): Int {
        var result = 0
        for (row in input.indices) {
            for (col in input[row].indices) {
                result += isXmas(input, row, col)
            }
        }

        return result
    }

    private fun isXmasX(input: List<String>, row: Int, col: Int): Boolean {
        if (input[row][col] != 'A') {
            return false
        }
        var c1 = getCharacter(input, row - 1, col - 1) // upper left
        var c2 = getCharacter(input, row + 1, col + 1) // lower right

        if (!isMas(c1, c2)) {
            return false
        }

        c1 = getCharacter(input, row - 1, col + 1) // upper right
        c2 = getCharacter(input, row + 1, col - 1) // lower left

        return isMas(c1, c2)
    }

    private fun getCharacter(input: List<String>, row: Int, col: Int): Char? {
        if (row < 0 || row >= input.size || col < 0 || col >= input[row].length) {
            return null
        }
        return input[row][col]
    }

    private fun isMas(c1: Char?, c2: Char?): Boolean {
        if (c1 == null || c2 == null) {
            return false
        }
        return c1 == 'M' && c2 == 'S' || c1 == 'S' && c2 == 'M'
    }

    private fun isXmas(input: List<String>, row: Int, col: Int): Int {
        if (input[row][col] != 'X') {
            return 0
        }
        var counter = 0
        for (d_col in -1..1) {
            for (d_row in -1..1) {
                if (d_col == 0 && d_row == 0) {
                    continue
                }
                val next_col = col + d_col
                val next_row = row + d_row

                if (isWord(input, next_row, next_col, Pair(d_col, d_row), "MAS")) {
                    counter += 1
                }
            }
        }

        return counter
    }

    private fun isWord(input: List<String>, row: Int, col: Int, vector: Pair<Int, Int>, word: String): Boolean {
        if (word.isEmpty()) {
            return true
        }
        if (row < 0 || row >= input.size || col < 0 || col >= input[row].length) {
            return false
        }
        if (input[row][col] != word[0]) {
            return false
        }
        val next_col = col + vector.first
        val next_row = row + vector.second

        return isWord(input, next_row, next_col, vector, word.substring(1))
    }
}