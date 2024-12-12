package de.pichlerj.utils

class Grid<T>(private val data: List<List<T>>) {

    val width: Int
    val height: Int

    init {
        require(data.isNotEmpty())
        require(data.all { it.size == data[0].size })

        width = data[0].size
        height = data.size
    }

    fun find(func: (T) -> Boolean): Sequence<Point> = sequence {
        for (y in data.indices) {
            for (x in data[y].indices) {
                if (func(data[y][x])) {
                    yield(Point(x, y))
                }
            }
        }
    }

    fun getNeighbors(point: Point, directions: List<Direction>, filter: (T) -> Boolean): Sequence<Point> {
        return getPoints(point, directions.map { it.toVector() }, filter)
    }

    fun getPoints(point: Point, vectors: List<Vector>, filter: (T) -> Boolean): Sequence<Point> = sequence {
        for (vector in vectors) {
            val next = point.addVector(vector)
            if (isInBounds(next) && filter(this@Grid[next])) {
                yield(next)
            }
        }
    }

    private fun isInBounds(point: Point): Boolean {
        return point.x in 0 until width && point.y in 0 until height
    }

    operator fun get(point: Point): T {
        return data[point.y][point.x]
    }

    fun getSafe(point: Point): T? {
        return if (isInBounds(point)) {
            get(point)
        } else {
            null
        }
    }
}

