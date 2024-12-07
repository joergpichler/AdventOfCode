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
        return input.filter { it.isValid(getOperations().take(2)) }.sumOf { it.result }
    }

    override fun solvePart02(input: List<Puzzle07Data>): Long {
        return input.filter { it.isValid(getOperations()) }.sumOf { it.result }
    }
}

class Puzzle07Data(val result: Long, val numbers: List<Long>) {
    fun isValid(operations: List<(Long, Long) -> Long>): Boolean {
        for(operation in operations) {
            if(isValid(operation(numbers[0], numbers[1]), numbers.drop(2), operations)){
                return true
            }
        }
        return false
    }

    private fun isValid(number: Long, numbers: List<Long>, operations: List<(Long, Long) -> Long>) : Boolean {
        if(numbers.isEmpty()) {
            return number == this.result
        }
        for(operation in operations) {
            if(isValid(operation(number, numbers[0]), numbers.drop(1), operations)){
                return true
            }
        }
        return false
    }
}

fun getOperations(): List<(Long, Long) -> Long> {
    return listOf(
        { a, b -> a + b },
        { a, b -> a * b },
        { a, b -> (a.toString() + b.toString()).toLong() }
    )
}