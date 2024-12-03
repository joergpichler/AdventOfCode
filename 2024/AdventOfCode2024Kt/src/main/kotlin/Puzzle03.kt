package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle03 : Puzzle<List<Instruction>, Int>(3, 2024) {
    override fun getTestData(): String {
        return "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    }

    override fun getTestData2(): String? {
        return "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    }

    override fun parse(input: String): List<Instruction> {
        val pattern = Regex("mul\\((\\d{1,3}),(\\d{1,3})\\)|do\\(\\)|don't\\(\\)")
        return pattern.findAll(input).map {
            if (it.groupValues[0].startsWith("mul")) {
                Mul(it.groupValues[1].toInt(), it.groupValues[2].toInt())
            } else if (it.groupValues[0].startsWith("don't")) {
                DoNot()
            } else {
                Do()
            }
        }.toList()
    }

    override fun solvePart02(input: List<Instruction>): Int {
        var sum = 0
        var enabled = true
        for (instruction in input) {
            when (instruction) {
                is Mul -> {
                    if (enabled) {
                        sum += instruction.execute()
                    }
                }

                is Do -> {
                    enabled = true
                }

                is DoNot -> {
                    enabled = false
                }
            }
        }
        return sum
    }

    override fun solvePart01(input: List<Instruction>): Int {
        return input.sumOf { it.execute() }
    }
}

interface Instruction {
    fun execute(): Int
}

class Mul(private val a: Int, private val b: Int) : Instruction {
    override fun execute(): Int {
        return a * b
    }
}

class Do : Instruction {
    override fun execute(): Int {
        return 0
    }
}

class DoNot : Instruction {
    override fun execute(): Int {
        return 0
    }
}