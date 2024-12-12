package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Grid
import de.pichlerj.utils.Point
import de.pichlerj.utils.getStraightNeighbors
import de.pichlerj.utils.straightDirections

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
        return Grid(input.lines().map { it.toList() })
    }

    override fun solvePart02(input: Grid<Char>): Long {
        TODO("Not yet implemented")
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

        for(x in 0 until grid.width){
            for(y in 0 until grid.height){
                val point = Point(x, y)

                if(regions.any { it.contains(point) }) {
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
        while(pointsToCheck.size > 0) {
            val currentPoint = pointsToCheck.first()
            pointsToCheck.remove(currentPoint)
            regionPoints.add(currentPoint)
            pointsToCheck.addAll(grid.getNeighbors(currentPoint, straightDirections(), { it == regionId }).filter { !regionPoints.contains(it) && !pointsToCheck.contains(it) })
        }

        return Region(regionId, regionPoints)
    }
}

class Region(val id: Char, private val points: Set<Point>) {

    private var perimeter: Int? = null

    fun getArea(): Int {
        return points.size
    }

    fun getPerimeter(): Int {
        if (perimeter != null) {
            return perimeter!!
        }
        var perimeter = 0

        val points = this.points.toMutableList()

        while (points.size > 0) {
            val point = points.removeFirst()
            perimeter += 4 - point.getStraightNeighbors().count { this.contains(it) }
        }

        this.perimeter = perimeter
        return perimeter
    }

    fun contains(point: Point): Boolean {
        return points.contains(point)
    }
}