package de.pichlerj.base

import java.nio.file.Paths
import kotlin.io.path.createDirectory
import kotlin.io.path.exists

abstract class Puzzle<TInput, TOutput>(private val day: Int, private val year: Int) {

    private val inputCache: InputCache

    init {
        val tmpDir = System.getProperty("java.io.tmpdir")
        val aocTmpDir = Paths.get(tmpDir, "AdventOfCode")
        if (!aocTmpDir.exists()) {
            aocTmpDir.createDirectory()
        }

        inputCache = InputCache(aocTmpDir.toString())
    }

    abstract fun getTestData(): String

    abstract fun parse(input: String): TInput

    abstract fun solvePart01(input: TInput): TOutput

    abstract fun solvePart02(input: TInput): TOutput

    open fun getTestData2(): String? {
        return null
    }

    fun runTest(part: Int = -1): Puzzle<TInput, TOutput> {
        val input = getTestData()
        val input2 = getTestData2()
        println("Test data")
        run(input, input2 ?: input, part)
        return this
    }

    fun run(part: Int = -1) {
        val input = inputCache.getInput(day, year).trimEnd()
        println("Input data")
        run(input, input, part)
    }

    private fun run(input: String, input2: String, part: Int): Puzzle<TInput, TOutput> {
        if (part == -1 || part == 1) {
            val parsedInput = parse(input)
            val resultPart01 = measureExecutionTime { solvePart01(parsedInput) }
            println("Pt1: ${resultPart01.first} (${resultPart01.second} ms)")
        }
        if (part == -1 || part == 2) {
            val parsedInput = parse(input2)
            val resultPart02 = try {
                measureExecutionTime { solvePart02(parsedInput) }
            } catch (exception: NotImplementedError) {
                Pair(null, -1)
            }
            println("Pt2: ${resultPart02.first} (${resultPart02.second} ms)")
        }
        return this
    }

    private fun <T> measureExecutionTime(block: () -> T): Pair<T, Long> {
        val startTime = System.currentTimeMillis()
        val result = block()
        val endTime = System.currentTimeMillis()
        val executionTime = endTime - startTime
        return Pair(result, executionTime)
    }
}