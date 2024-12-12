package de.pichlerj.utils

enum class Direction {
    Left,
    UpperLeft,
    Up,
    UpperRight,
    Right,
    LowerRight,
    Down,
    LowerLeft
}

fun horizontalDirections(): List<Direction> {
    return listOf(Direction.Left, Direction.Right)
}

fun verticalDirections(): List<Direction> {
    return listOf(Direction.Up, Direction.Down)
}

fun straightDirections(): List<Direction> {
    return listOf(Direction.Left, Direction.Up, Direction.Right, Direction.Down)
}

fun diagonalDirections(): List<Direction> {
    return listOf(Direction.UpperLeft, Direction.UpperRight, Direction.LowerRight, Direction.LowerLeft)
}

fun allDirections(): List<Direction> {
    return Direction.entries
}

fun Direction.toVector(): Vector {
    return when (this) {
        Direction.Left -> Vector(-1, 0)
        Direction.UpperLeft -> Vector(-1, -1)
        Direction.Up -> Vector(0, -1)
        Direction.UpperRight -> Vector(1, -1)
        Direction.Right -> Vector(1, 0)
        Direction.LowerRight -> Vector(1, 1)
        Direction.Down -> Vector(0, 1)
        Direction.LowerLeft -> Vector(-1, 1)
    }
}