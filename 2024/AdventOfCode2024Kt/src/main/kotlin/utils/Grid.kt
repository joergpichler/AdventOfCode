package de.pichlerj.utils

class Grid<T>(private val data: List<MutableList<T>>) {

    val width: Int
    val height: Int

    init {
        require(data.isNotEmpty())
        require(data.all { it.size == data[0].size })

        width = data[0].size
        height = data.size
    }

    fun find(func: (T) -> Boolean): Point? {
        for (y in data.indices) {
            for (x in data[y].indices) {
                if (func(data[y][x])) {
                    return Point(x, y)
                }
            }
        }
        return null
    }

    fun findAll(func: (T) -> Boolean): Sequence<Point> = sequence {
        for (y in data.indices) {
            for (x in data[y].indices) {
                if (func(data[y][x])) {
                    yield(Point(x, y))
                }
            }
        }
    }

    fun findFromAlong(
        startingPoint: Point,
        along: Vector,
        func: (T) -> Boolean,
        funcAbort: ((T) -> Boolean)? = null
    ): Point? {
        var current = startingPoint.addVector(along)
        while (isInBounds(current)) {
            if (funcAbort != null && funcAbort(this[current])) {
                return null
            }
            if (func(this[current])) {
                return current
            }
            current = current.addVector(along)
        }
        return null
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

    fun get(row: Int, col: Int) : T {
        return data[row][col]
    }

    fun getSafe(point: Point): T? {
        return if (isInBounds(point)) {
            get(point)
        } else {
            null
        }
    }

    operator fun set(position: Point, value: T) {
        data[position.y][position.x] = value
    }

    fun print() {
        for (y in data.indices) {
            for (x in data[y].indices) {
                print(data[y][x])
            }
            println()
        }
    }
}

