package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Point

class Puzzle06 : Puzzle<Puzzle06Data, Int>(6, 2024) {
    override fun getTestData(): String {
        return "....#.....\n" +
                ".........#\n" +
                "..........\n" +
                "..#.......\n" +
                ".......#..\n" +
                "..........\n" +
                ".#..^.....\n" +
                "........#.\n" +
                "#.........\n" +
                "......#..."
    }

    override fun parse(input: String): Puzzle06Data {
        val lines = input.split("\n")
        val sizeX = lines[0].length
        val sizeY = lines.size
        val obstructions = mutableListOf<Point>()
        var guardPosition: Point? = null
        for (y in lines.indices) {
            for (x in lines[y].indices) {
                val c = lines[y][x]
                if (c == '^') {
                    guardPosition = Point(x, y)
                } else if (c == '#') {
                    obstructions.add(Point(x, y))
                }
            }
        }
        if (guardPosition == null) {
            throw Exception("Guard position not found")
        }
        return Puzzle06Data(MapData(sizeX, sizeY, obstructions.toSet()), Guard(guardPosition!!, Direction.UP))
    }


    override fun solvePart02(input: Puzzle06Data): Int {
        val mapData = input.mapData
        val guard = input.guard

        var result = 0

        for (x in 0 until mapData.sizeX) {
            for (y in 0 until mapData.sizeY) {
                val point = Point(x, y)
                if (mapData.isObstructed(point) || guard.position == point) {
                    continue
                }
                val newObstructions = mapData.obstructions.toMutableSet()
                newObstructions.add(point)
                val newMapData = MapData(mapData.sizeX, mapData.sizeY, newObstructions)
                val newGuard = guard.clone()
                if (solve(newMapData, newGuard) == -1) {
                    result += 1
                }
            }
        }

        return result
    }

    override fun solvePart01(input: Puzzle06Data): Int {
        val mapData = input.mapData
        val guard = input.guard

        return solve(mapData, guard)
    }

    private fun solve(mapData: MapData, guard: Guard): Int {
        val guardPositions = mutableSetOf<Point>()
        val guardTrace = mutableSetOf<GuardState>()

        while (mapData.isInBounds(guard.position)) {
            if (!guardTrace.add(guard.state())) {
                return -1
            }
            guardPositions.add(guard.position)
            var nextPosition = guard.position.next(guard.direction)
            while (mapData.isObstructed(nextPosition)) {
                guard.direction = when (guard.direction) {
                    Direction.UP -> Direction.RIGHT
                    Direction.RIGHT -> Direction.DOWN
                    Direction.DOWN -> Direction.LEFT
                    Direction.LEFT -> Direction.UP
                }
                nextPosition = guard.position.next(guard.direction)
            }
            guard.position = nextPosition
        }

        return guardPositions.size
    }

}

data class Puzzle06Data(val mapData: MapData, val guard: Guard)

class Guard(var position: Point, var direction: Direction) {
    fun clone(): Guard {
        return Guard(position.copy(), direction)
    }

    fun state(): GuardState {
        return GuardState(position, direction)
    }
}

enum class Direction {
    UP, DOWN, LEFT, RIGHT
}

data class GuardState(val position: Point, val direction: Direction)

class MapData(val sizeX: Int, val sizeY: Int, val obstructions: Set<Point>) {
    fun isObstructed(point: Point): Boolean {
        return obstructions.contains(point)
    }

    fun isInBounds(point: Point): Boolean {
        return point.x in 0..<sizeX && point.y in 0..<sizeY
    }
}

fun Point.next(direction: Direction): Point {
    return when (direction) {
        Direction.UP -> Point(x, y - 1)
        Direction.DOWN -> Point(x, y + 1)
        Direction.LEFT -> Point(x - 1, y)
        Direction.RIGHT -> Point(x + 1, y)
    }
}
