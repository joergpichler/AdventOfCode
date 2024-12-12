package de.pichlerj.utils

data class Point(val x: Int, val y: Int){
    operator fun minus(other: Point): Vector {
        return Vector(this.x - other.x, this.y - other.y)
    }

    fun addVector(vector: Vector): Point {
        return Point(this.x + vector.dx, this.y + vector.dy)
    }
}

fun Point.getStraightNeighbors(): List<Point> {
    return straightDirections().map { it.toVector() }.map { this.addVector(it) }
}

fun Point.up(): Point {
    return Point(this.x, this.y - 1)
}

fun Point.down(): Point {
    return Point(this.x, this.y + 1)
}

fun Point.left(): Point {
    return Point(this.x - 1, this.y)
}

fun Point.right(): Point {
    return Point(this.x + 1, this.y)
}