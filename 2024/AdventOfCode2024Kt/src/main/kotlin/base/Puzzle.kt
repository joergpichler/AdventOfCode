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

    open fun getTestData2() : String? {
        return null
    }

    fun runTest(): Puzzle<TInput, TOutput> {
        val input = getTestData()
        val input2 = getTestData2()
        println("Test data")
        run(input, input2 ?: input)
        return this
    }

    fun run() {
        val input = inputCache.getInput(day, year).trimEnd()
        println("Input data")
        run(input, input)
    }

    private fun run(input: String, input2: String): Puzzle<TInput, TOutput> {
        var parsedInput = parse(input)
        val resultPart01 = measureExecutionTime { solvePart01(parsedInput) }
        println("Pt1: ${resultPart01.first} (${resultPart01.second} ms)")
        parsedInput = parse(input2)
        val resultPart02 = measureExecutionTime { solvePart02(parsedInput) }
        println("Pt2: ${resultPart02.first} (${resultPart02.second} ms)")
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