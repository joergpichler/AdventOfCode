package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.Direction
import de.pichlerj.utils.Grid
import de.pichlerj.utils.Point
import de.pichlerj.utils.Vector
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

//        return "########\n" +
//                "#..O.O.#\n" +
//                "##@.O..#\n" +
//                "#...O..#\n" +
//                "#.#.O..#\n" +
//                "#...O..#\n" +
//                "#......#\n" +
//                "########\n" +
//                "\n" +
//                "<^^>>>vv<v>>v<<"
//
//        return "#######\n" +
//                "#...#.#\n" +
//                "#.....#\n" +
//                "#..OO@#\n" +
//                "#..O..#\n" +
//                "#.....#\n" +
//                "#######\n" +
//                "\n" +
//                "<vv<<^^<<^^"
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
        val newGrid = transformGrid(input.grid)
        var robotPosition = newGrid.find { it == '@' }!!
        for (movement in input.movements) {
//            newGrid.print()
//            println("next move: $movement")
//            readLine()
            robotPosition = move(newGrid, robotPosition, movement)
        }
        newGrid.print()
        return newGrid.findAll { it == '[' }.sumOf { it.x + 100 * it.y }
    }

    private fun transformGrid(grid: Grid<Char>): Grid<Char> {
        val rows = mutableListOf<MutableList<Char>>()

        for (idxRow in 0 until grid.height) {
            val row = mutableListOf<Char>()
            for (idxCol in 0 until grid.width) {
                val char = grid.get(idxRow, idxCol)
                if (char == '#') {
                    row.add('#')
                    row.add('#')
                } else if (char == 'O') {
                    row.add('[')
                    row.add(']')
                } else if (char == '.') {
                    row.add('.')
                    row.add('.')
                } else if (char == '@') {
                    row.add('@')
                    row.add('.')
                } else {
                    throw IllegalArgumentException()
                }
            }
            rows.add(row)
        }

        return Grid(rows)
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

//        grid.print()

        return grid.findAll { it == 'O' }.sumOf { it.x + 100 * it.y }
    }

    private fun move(grid: Grid<Char>, robotPosition: Point, movement: Char): Point {
        val direction = when (movement) {
            '^' -> Direction.Up
            'v' -> Direction.Down
            '<' -> Direction.Left
            '>' -> Direction.Right
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
        if (Box.isBoxChar(newPositionChar)) {
            val box = Box(newPosition, grid)
            return if (box.move(direction)) {
                assert(grid[newPosition] == '.')
                grid[robotPosition] = '.'
                grid[newPosition] = '@'
                newPosition
            } else {
                robotPosition
            }
//            val freeSpace = grid.findFromAlong(robotPosition, direction, { it == '.' }, { it == '#' })
//            if (freeSpace == null) {
//                return robotPosition
//            } else {
//                grid[robotPosition] = '.'
//                grid[newPosition] = '@'
//                grid[freeSpace] = 'O'
//                return newPosition
//            }
        }
        throw IllegalStateException("Invalid position: $newPositionChar")
    }
}

data class Puzzle15Data(val grid: Grid<Char>, val movements: List<Char>)

class Box(point: Point, private val grid: Grid<Char>) {

    private val points: List<Point>

    init {
        points = if (grid[point] == 'O') {
            listOf(point)
        } else {
            if (grid[point] == '[') {
                listOf(point, point.addVector(Direction.Right.toVector()))
            } else if (grid[point] == ']') {
                listOf(point.addVector(Direction.Left.toVector()), point)
            } else {
                throw IllegalStateException()
            }
        }
    }

    fun move(vector: Vector, test: Boolean = false): Boolean {
        if (points.size == 1) {
            return moveSimple(vector)
        } else {
            return moveComplex(vector, test)
        }
    }

    private fun moveComplex(vector: Vector, test: Boolean): Boolean {
        if (vector.dx == -1) { // left
            assert(!test)
            return moveComplexLeft()
        } else if (vector.dx == 1) { // right
            assert(!test)
            return moveComplexRight()
        } else if (vector.dy != 0) { // up
            return moveVertical(vector, test)
        } else {
            throw IllegalStateException()
        }
    }

    private fun moveComplexLeft(): Boolean {
        val vector = Direction.Left.toVector()
        val nextPoint = points[0].addVector(vector)
        val leftChar = grid[nextPoint]
        if (leftChar == '.' || (isBoxChar(leftChar) && Box(nextPoint, grid).move(vector))) {
            grid[nextPoint] = '['
            grid[points[0]] = ']'
            grid[points[1]] = '.'
            return true
        } else {
            return false
        }
    }

    private fun moveComplexRight(): Boolean {
        val vector = Direction.Right.toVector()
        val nextPoint = points[1].addVector(vector)
        val rightChar = grid[nextPoint]
        if (rightChar == '.' || (isBoxChar(rightChar) && Box(nextPoint, grid).move(vector))) {
            grid[nextPoint] = ']'
            grid[points[1]] = '['
            grid[points[0]] = '.'
            return true
        } else {
            return false
        }
    }

    private fun moveVertical(vector: Vector, test: Boolean): Boolean {
        val nextPoints = points.map { it.addVector(vector) }
        val nextChars = nextPoints.map { grid[it] }
        var moveMe = false
        if (nextChars.all { it == '.' }) {
            moveMe = true
        } else if (nextChars[0] == '[' && nextChars[1] == ']') {
            val nextBox = Box(nextPoints[0], grid)
            moveMe = nextBox.move(vector)
        } else if (nextChars[0] == ']' && nextChars[1] == '[') {
            val nextBox1 = Box(nextPoints[0], grid)
            val nextBox2 = Box(nextPoints[1], grid)
            moveMe = nextBox1.move(vector, true) && nextBox2.move(vector, true)
            if (moveMe) {
                assert(nextBox1.move(vector) && nextBox2.move(vector))
            }
        } else if (nextChars.any { it == '#' }) {
            return false
        } else if (nextChars[0] == ']' && nextChars[1] == '.') {
            val nextBox = Box(nextPoints[0], grid)
            moveMe = nextBox.move(vector, test)
            if (moveMe) {
                assert(nextBox.move(vector))
            }
        } else if (nextChars[0] == '.' && nextChars[1] == '[') {
            val nextBox = Box(nextPoints[1], grid)
            moveMe = nextBox.move(vector, test)
            if (moveMe) {
                assert(nextBox.move(vector))
            }
        } else {
            throw IllegalStateException()
        }
        if (moveMe) {
            if (!test) {
                grid[nextPoints[0]] = '['
                grid[nextPoints[1]] = ']'
                grid[points[0]] = '.'
                grid[points[1]] = '.'
            }
            return true
        }
        return false
    }

    private fun moveSimple(vector: Vector): Boolean {
        val point = points[0]
        val nextPoint = point.addVector(vector)
        val char = grid[nextPoint]
        var moveMe = false
        if (isBoxChar(char)) {
            val nextBox = Box(nextPoint, grid)
            if (nextBox.move(vector)) {
                moveMe = true
            }
        } else if (char == '#') {
            return false
        } else if (char == '.') {
            moveMe = true
        }
        if (moveMe) {
            assert(grid[nextPoint] == '.')
            grid[nextPoint] = 'O'
            grid[point] = '.'
            return true
        }
        return false
    }

    companion object {
        fun isBoxChar(char: Char): Boolean {
            return char == 'O' || char == '[' || char == ']'
        }
    }


}