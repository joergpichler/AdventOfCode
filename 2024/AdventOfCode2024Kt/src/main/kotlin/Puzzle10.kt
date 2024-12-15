package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Grid
import de.pichlerj.utils.Point
import de.pichlerj.utils.straightDirections

class Puzzle10 : Puzzle<Grid<Int>, Int>(10, 2024) {
    override fun getTestData(): String {
        return "89010123\n" +
                "78121874\n" +
                "87430965\n" +
                "96549874\n" +
                "45678903\n" +
                "32019012\n" +
                "01329801\n" +
                "10456732"
    }

    override fun parse(input: String): Grid<Int> {
        return Grid(input.lines().map { line ->
            line.map {
                val s = it.toString()
                if (s == ".") {
                    -1
                } else {
                    s.toInt()
                }
            }.toMutableList()
        })
    }

    override fun solvePart02(input: Grid<Int>): Int {
        return solve(input, { it.size })
    }

    override fun solvePart01(input: Grid<Int>): Int {
        return solve(input, { it.distinctBy { it.last() }.size })
    }

    private fun solve(input: Grid<Int>, trailsCounter: (List<List<Point>>) -> Int): Int {
        var result = 0
        for (startLocation in input.findAll { it == 0 }) {

            val possibleTrails = mutableListOf<MutableList<Point>>()
            possibleTrails.add(mutableListOf(startLocation))

            var trailsUpdated = true
            while (trailsUpdated) {
                trailsUpdated = false

                val trailsCopy = possibleTrails.toList()
                possibleTrails.clear()
                for (trail in trailsCopy) {
                    val trailValue = input.get(trail.last())
                    if (trailValue == 9) {
                        possibleTrails.add(trail)
                        continue
                    }
                    val nextPoints =
                        input.getNeighbors(trail.last(), straightDirections(), { it == trailValue + 1 }).toList()
                    if (nextPoints.isNotEmpty()) {
                        trailsUpdated = true
                        for (nextPoint in nextPoints) {
                            val newTrail = trail.toMutableList()
                            newTrail.add(nextPoint)
                            possibleTrails.add(newTrail)
                        }
                    }
                }
            }
//            for (trail in possibleTrails) {
//                println(trail)
//            }
            result += trailsCounter(possibleTrails)
        }
        return result
    }
}