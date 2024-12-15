package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.*

class Puzzle12 : Puzzle<Grid<Char>, Long>(12, 2024) {
    override fun getTestData(): String {
        return "RRRRIICCFF\n" +
                "RRRRIICCCF\n" +
                "VVRRRCCFFF\n" +
                "VVRCCCJFFF\n" +
                "VVVVCJJCFE\n" +
                "VVIVCCJJEE\n" +
                "VVIIICJJEE\n" +
                "MIIIIIJJEE\n" +
                "MIIISIJEEE\n" +
                "MMMISSJEEE"
    }

    override fun parse(input: String): Grid<Char> {
        return Grid(input.lines().map { it.toMutableList() })
    }

    override fun solvePart02(input: Grid<Char>): Long {
        val regions = getRegions(input)
        var result = 0L
        for (region in regions) {
            val regionPrice = region.getArea() * region.getNumberOfSides()
            result += regionPrice
        }
        return result
    }

    override fun solvePart01(input: Grid<Char>): Long {
        val regions = getRegions(input)
        var result = 0L
        for (region in regions) {
            val regionPrice = region.getArea() * region.getPerimeter()
            result += regionPrice
        }
        return result
    }

    private fun getRegions(grid: Grid<Char>): List<Region> {
        val regions = mutableListOf<Region>()

        for (x in 0 until grid.width) {
            for (y in 0 until grid.height) {
                val point = Point(x, y)

                if (regions.any { it.contains(point) }) {
                    continue
                }

                regions.add(getRegion(grid, point))
            }
        }

        return regions
    }

    private fun getRegion(grid: Grid<Char>, point: Point): Region {
        val regionId = grid[point]
        val regionPoints = mutableSetOf<Point>()

        val pointsToCheck = mutableSetOf(point)
        while (pointsToCheck.size > 0) {
            val currentPoint = pointsToCheck.first()
            pointsToCheck.remove(currentPoint)
            regionPoints.add(currentPoint)
            pointsToCheck.addAll(
                grid.getNeighbors(currentPoint, straightDirections(), { it == regionId })
                    .filter { !regionPoints.contains(it) && !pointsToCheck.contains(it) })
        }

        return Region(regionId, regionPoints)
    }
}

class Region(val id: Char, private val points: Set<Point>) {

    fun getArea(): Int {
        return points.size
    }

    fun getPerimeter(): Int {
        var perimeter = 0

        val points = this.points.toMutableList()

        while (points.size > 0) {
            val point = points.removeFirst()
            perimeter += 4 - point.getStraightNeighbors().count { this.contains(it) }
        }

        return perimeter
    }

    fun contains(point: Point): Boolean {
        return points.contains(point)
    }

    fun getNumberOfSides(): Int {
        var sides = 0

        val topEdges = mutableSetOf<Point>()
        val bottomEdges = mutableSetOf<Point>()
        val leftEdges = mutableSetOf<Point>()
        val rightEdges = mutableSetOf<Point>()

        for (point in points) {
            if (!points.contains(point.up())) {
                topEdges.add(point)
            }
            if (!points.contains(point.down())) {
                bottomEdges.add(point)
            }
            if (!points.contains(point.left())) {
                leftEdges.add(point)
            }
            if (!points.contains(point.right())) {
                rightEdges.add(point)
            }
        }

        sides += getHorizontalSides(topEdges)
        sides += getHorizontalSides(bottomEdges)
        sides += getVerticalSides(leftEdges)
        sides += getVerticalSides(rightEdges)

        return sides
    }

    private fun getHorizontalSides(horizontalEdges: MutableSet<Point>): Int {
        var sides = 0
        while(horizontalEdges.size > 0) {
            val point = horizontalEdges.first()
            horizontalEdges.remove(point)
            sides += 1
            var next = point.left()
            while(horizontalEdges.contains(next)) {
                horizontalEdges.remove(next)
                next = next.left()
            }
            next = point.right()
            while(horizontalEdges.contains(next)) {
                horizontalEdges.remove(next)
                next = next.right()
            }
        }
        return sides
    }

    private fun getVerticalSides(verticalEdges: MutableSet<Point>): Int {
        var sides = 0
        while(verticalEdges.size > 0) {
            val point = verticalEdges.first()
            verticalEdges.remove(point)
            sides += 1
            var next = point.up()
            while(verticalEdges.contains(next)) {
                verticalEdges.remove(next)
                next = next.up()
            }
            next = point.down()
            while(verticalEdges.contains(next)) {
                verticalEdges.remove(next)
                next = next.down()
            }
        }
        return sides
    }

}