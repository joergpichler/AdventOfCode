package de.pichlerj.base

import java.nio.file.Paths
import kotlin.io.path.createDirectory
import kotlin.io.path.createTempDirectory
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

    fun runTest(): Puzzle<TInput, TOutput> {
        val input = getTestData()
        run(input)
        return this
    }

    fun run() {
        val input = inputCache.getInput(day, year).trimEnd()
        run(input)
    }

    private fun run(input: String): Puzzle<TInput, TOutput> {
        var parsedInput = parse(input)
        val resultPart01 = solvePart01(parsedInput)
        println(resultPart01)
        parsedInput = parse(input)
        val resultPart02 = solvePart02(parsedInput)
        println(resultPart02)
        return this
    }
}