package de.pichlerj

import de.pichlerj.base.Puzzle
import de.pichlerj.utils.*
import kotlin.math.abs

class Puzzle16 : Puzzle<Grid<Char>, Int>(16, 2024) {
    override fun getTestData(): String {
        return "###############\n" +
                "#.......#....E#\n" +
                "#.#.###.#.###.#\n" +
                "#.....#.#...#.#\n" +
                "#.###.#####.#.#\n" +
                "#.#.#.......#.#\n" +
                "#.#.#####.###.#\n" +
                "#...........#.#\n" +
                "###.#.#####.#.#\n" +
                "#...#.....#.#.#\n" +
                "#.#.#.###.#.#.#\n" +
                "#.....#...#.#.#\n" +
                "#.###.#.#.#.#.#\n" +
                "#S..#.....#...#\n" +
                "###############"
    }

    override fun parse(input: String): Grid<Char> {
        return Grid(input.lines().map { it.toCharArray().toMutableList() })
    }

    override fun solvePart02(input: Grid<Char>): Int {
        TODO("Not yet implemented")
    }

    override fun solvePart01(input: Grid<Char>): Int {
        val graph = Puzzle16Graph(input)
        val start = input.find { it == 'S' }!!
        val end = input.find { it == 'E' }!!
        val dijkstra = Dijkstra(graph)
        val path = dijkstra.shortestPath(start, end)
        // convert path into vectors
        val vectors = path.zipWithNext { a, b -> b - a }

        var currentDirection = if(vectors[0].dx != 0) 'x' else 'y'
        var score = if(currentDirection == 'x') 0 else 1000
        for(vector in vectors) {
            val direction = if(vector.dx != 0) 'x' else 'y'
            if(direction == currentDirection) {
                score += 1
            } else {
                score += 1001
            }
            currentDirection = direction
        }
        return score
    }
}

class Puzzle16Graph(private val graph: Grid<Char>) : Graph<Point> {

    override fun vertices(): List<Point> {
        return graph.findAll { it != '#' }.toList()
    }

    override fun edgeWeight(from: Point, to: Point, pathHistory: List<Point>): Double {
        val vector = to - from
        assert(abs(vector.dx) + abs(vector.dy) == 1)
        var includesRotation = false
        if(pathHistory.size > 1) {
            val lastVector = pathHistory[pathHistory.size - 1] - pathHistory[pathHistory.size - 2]
            if(abs(vector.dx) != abs(lastVector.dx) || abs(vector.dy) != abs(lastVector.dy)) {
                includesRotation = true
            }
        }
        var result = 1.0
        if(includesRotation) {
            result += 1000
        }
        return result
    }

    override fun adjacents(vertex: Point): List<Point> {
        return graph.getNeighbors(vertex, straightDirections(), { it != '#' }).toList()
    }


}