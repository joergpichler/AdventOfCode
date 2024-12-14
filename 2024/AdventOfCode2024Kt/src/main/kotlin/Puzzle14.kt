package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Point
import de.pichlerj.utils.Vector

class Puzzle14 : Puzzle<List<Robot>, Int>(14, 2024) {
    override fun getTestData(): String {
        return "p=0,4 v=3,-3\n" +
                "p=6,3 v=-1,-3\n" +
                "p=10,3 v=-1,2\n" +
                "p=2,0 v=2,-1\n" +
                "p=0,0 v=1,3\n" +
                "p=3,0 v=-2,-2\n" +
                "p=7,6 v=-1,-3\n" +
                "p=3,0 v=-1,-2\n" +
                "p=9,3 v=2,3\n" +
                "p=7,3 v=-1,2\n" +
                "p=2,4 v=2,-3\n" +
                "p=9,5 v=-3,-3"
    }

    override fun parse(input: String): List<Robot> {
        return input.lines().map {
            val parts = it.split(" ")
            val p = parts[0].substringAfter("p=").split(",").map { it.toInt() }
            val v = parts[1].substringAfter("v=").split(",").map { it.toInt() }
            Robot(Point(p[0], p[1]), Vector(v[0], v[1]))
        }
    }

    override fun solvePart02(input: List<Robot>): Int {
        val gridWidth = 101
        val gridHeight = 103

        var ctr = 1
        while (true) {
            val robotPositions = run(gridWidth, gridHeight, input, ctr).toHashSet()

            if (robotPositions.any { it ->
                    val a1 = Point(it.x - 1, it.y - 1)
                    val a2 = Point(it.x, it.y - 1)
                    val a3 = Point(it.x + 1, it.y - 1)
                    val b1 = Point(a1.x - 1, a1.y - 1)
                    val b2 = Point(a1.x, a1.y - 1)
                    val b3 = Point(a1.x + 1, a1.y - 1)
                    val b4 = Point(a3.x, a3.y - 1)
                    val b5 = Point(a3.x + 1, a3.y - 1)
                    robotPositions.containsAll(listOf(a1, a2, a3, b1, b2, b3, b4, b5))
                }) {
                println(ctr)
                debugPrint(gridWidth, gridHeight, robotPositions.toList())
                return ctr
            } else {
                ctr += 1
            }
        }

    }

    override fun solvePart01(input: List<Robot>): Int {
        val gridWidth = 101
        val gridHeight = 103

        val robotPositions = run(gridWidth, gridHeight, input, 100)

        // count how many robots are in each quadrant, the middle lines are excluded
        val quadrantWidth = gridWidth / 2
        val quadrantHeight = gridHeight / 2
        val quadrants = robotPositions.groupBy {
            when {
                it.x < quadrantWidth && it.y < quadrantHeight -> 1
                it.x > quadrantWidth && it.y < quadrantHeight -> 2
                it.x > quadrantWidth && it.y > quadrantHeight -> 3
                it.x < quadrantWidth && it.y > quadrantHeight -> 4
                else -> -1
            }
        }

        return quadrants[1]!!.size * quadrants[2]!!.size * quadrants[3]!!.size * quadrants[4]!!.size
    }

    private fun run(gridWidth: Int, gridHeight: Int, robots: List<Robot>, seconds: Int): MutableList<Point> {
        val robotPositions = mutableListOf<Point>()

        for (robot in robots) {
            val vector = robot.v.multiply(seconds)
            val point = robot.p.addVector(vector)
            //wrap point into grid dimensions
            val wrappedPoint = Point(
                (point.x % gridWidth + gridWidth) % gridWidth,
                (point.y % gridHeight + gridHeight) % gridHeight
            )
            robotPositions.add(wrappedPoint)
        }

        return robotPositions
    }

    private fun debugPrint(gridWidth: Int, gridHeight: Int, robotPositions: List<Point>) {
        for (y in 0 until gridHeight) {
            for (x in 0 until gridWidth) {
                val countRobots = robotPositions.count { it.x == x && it.y == y }
                print(if (countRobots > 0) "$countRobots" else ".")
            }
            println()
        }
    }
}

data class Robot(val p: Point, val v: Vector)