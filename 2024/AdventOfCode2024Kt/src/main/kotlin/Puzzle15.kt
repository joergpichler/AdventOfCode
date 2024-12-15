package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Grid
import de.pichlerj.utils.Point
import de.pichlerj.utils.toVector

class Puzzle15 : Puzzle<Puzzle15Data, Int>(15, 2024) {
    override fun getTestData(): String {
        return "##########\n" +
                "#..O..O.O#\n" +
                "#......O.#\n" +
                "#.OO..O.O#\n" +
                "#..O@..O.#\n" +
                "#O#..O...#\n" +
                "#O..O..O.#\n" +
                "#.OO.O.OO#\n" +
                "#....O...#\n" +
                "##########\n" +
                "\n" +
                "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\n" +
                "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n" +
                "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n" +
                "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n" +
                "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n" +
                "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n" +
                ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n" +
                "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n" +
                "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\n" +
                "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
    }

    override fun parse(input: String): Puzzle15Data {
        val lines = input.lines()
        // find index of empty line
        val emptyLineIndex = lines.indexOfFirst { it.isBlank() }
        val grid = Grid(lines.slice(0 until emptyLineIndex).map { it.toCharArray().toMutableList() })
        val movements = lines.slice(emptyLineIndex + 1 until lines.size).flatMap { it.toCharArray().toList() }
        return Puzzle15Data(grid, movements)
    }

    override fun solvePart02(input: Puzzle15Data): Int {
        TODO("Not yet implemented")
    }

    override fun solvePart01(input: Puzzle15Data): Int {
        val (grid, movements) = input
        var robotPosition = grid.find { it == '@' }!!

//        grid.print()

        for (movement in movements) {
            robotPosition = move(grid, robotPosition, movement)
//            readLine()
//            grid.print()
        }

        grid.print()

        return grid.findAll { it == 'O' }.sumOf { it.x + 100 * it.y }
    }

    private fun move(grid: Grid<Char>, robotPosition: Point, movement: Char): Point {
        val direction = when (movement) {
            '^' -> de.pichlerj.utils.Direction.Up
            'v' -> de.pichlerj.utils.Direction.Down
            '<' -> de.pichlerj.utils.Direction.Left
            '>' -> de.pichlerj.utils.Direction.Right
            else -> throw IllegalArgumentException("Invalid movement: $movement")
        }.toVector()

        val newPosition = robotPosition.addVector(direction)

        val newPositionChar = grid[newPosition]
        if (newPositionChar == '.') {
            grid[robotPosition] = '.'
            grid[newPosition] = '@'
            return newPosition
        }
        if (newPositionChar == '#') {
            return robotPosition
        }
        if (newPositionChar == 'O') {
            val freeSpace = grid.findFromAlong(robotPosition, direction, { it == '.' }, { it == '#' })
            if (freeSpace == null) {
                return robotPosition
            } else {
                grid[robotPosition] = '.'
                grid[newPosition] = '@'
                grid[freeSpace] = 'O'
                return newPosition
            }
        }
        throw IllegalStateException("Invalid position: $newPositionChar")
    }
}

data class Puzzle15Data(val grid: Grid<Char>, val movements: List<Char>)