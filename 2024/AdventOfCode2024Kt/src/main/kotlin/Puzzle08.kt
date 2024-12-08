package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Point

class Puzzle08 : Puzzle<Puzzle08Data, Int>(8, 2024) {
    override fun getTestData(): String {
        return "............\n" +
                "........0...\n" +
                ".....0......\n" +
                ".......0....\n" +
                "....0.......\n" +
                "......A.....\n" +
                "............\n" +
                "............\n" +
                "........A...\n" +
                ".........A..\n" +
                "............\n" +
                "............"
    }

    override fun parse(input: String): Puzzle08Data {
        return Puzzle08Data(input.lines())
    }

    override fun solvePart02(input: Puzzle08Data): Int {
        return input.getUniqueAntinodesPt2().size
    }

    override fun solvePart01(input: Puzzle08Data): Int {
        return input.getUniqueAntinodesPt1().size
    }
}

class Puzzle08Data(val map: List<String>) {

    private val frequencies: List<Frequency>

    init {
        val frequencies = HashMap<Char, MutableList<Point>>()
        for (y in map.indices) {
            val line = map[y]
            for (x in line.indices) {
                val c = line[x]
                if (c != '.') {
                    frequencies.getOrPut(c, { mutableListOf() }).add(Point(x, y))
                }
            }
        }
        this.frequencies = frequencies.map { Frequency(it.key, it.value) }
    }

    fun getUniqueAntinodesPt1(): Set<Point> {
        val result = mutableSetOf<Point>()

        for (frequency in frequencies) {
            for (antinode in frequency.getAntinodesPt1(::isPointInMap)) {
                    result.add(antinode)
            }
        }

        return result
    }

    fun getUniqueAntinodesPt2(): Set<Point> {
        val result = mutableSetOf<Point>()

        for (frequency in frequencies) {
            for (antinode in frequency.getAntinodesPt2(::isPointInMap)) {
                result.add(antinode)
            }
        }

        return result
    }

    private fun isPointInMap(point: Point): Boolean {
        return point.x >= 0 && point.x < map[0].length && point.y >= 0 && point.y < map.size
    }
}

data class Frequency(val id: Char, val points: List<Point>) {
    fun getAntinodesPt1(func: (Point) -> Boolean): Sequence<Point> = sequence {
        for (i in points.indices) {
            val pointA = points[i]
            for (j in i + 1 until points.size) {
                val pointB = points[j]
                val vectorAB = (pointB - pointA).multiply(2)
                val vectorBA = vectorAB.invert()

                val candidateA = pointA.addVector(vectorAB)
                val candidateB = pointB.addVector(vectorBA)

                if (func(candidateA)) {
                    yield(candidateA)
                }
                if (func(candidateB)) {
                    yield(candidateB)
                }
            }
        }
    }

    fun getAntinodesPt2(func: (Point) -> Boolean): Sequence<Point> = sequence {
        for (i in points.indices) {
            val pointA = points[i]
            for (j in i + 1 until points.size) {
                val pointB = points[j]
                val vectorAB = (pointB - pointA)
                yield(pointA)
                yield(pointB)
                // forward
                var next = pointB.addVector(vectorAB)
                while(func(next)){
                    yield(next)
                    next = next.addVector(vectorAB)
                }
                // backward
                val vectorBA = vectorAB.invert()
                next = pointA.addVector(vectorBA)
                while(func(next)){
                    yield(next)
                    next = next.addVector(vectorBA)
                }
            }
        }
    }
}