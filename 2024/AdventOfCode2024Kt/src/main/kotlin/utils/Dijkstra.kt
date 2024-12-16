package de.pichlerj.utils

class Dijkstra<T>(private val graph: Graph<T>) {
    /**
     * Finds the shortest path from start to end vertex using Dijkstra's algorithm, considering path history.
     * @param start The starting vertex.
     * @param end The target vertex.
     * @return A list of vertices representing the shortest path or an empty list if no path exists.
     */
    fun shortestPath(start: T, end: T): List<T> {
        // Data structures for Dijkstra's algorithm
        val distances = mutableMapOf<T, Double>().withDefault { Double.POSITIVE_INFINITY }
        val previous = mutableMapOf<T, T?>()
        val unvisited = graph.vertices().toMutableSet()

        distances[start] = 0.0

        while (unvisited.isNotEmpty()) {
            val current = unvisited.minByOrNull { distances.getValue(it) } ?: break
            if (current == end) break

            unvisited.remove(current)

            for (neighbor in graph.adjacents(current)) {
                if (neighbor in unvisited) {
                    // Reconstruct the path history up to the current vertex
                    val pathHistory = reconstructPath(previous, start, current)
                    val newDistance = distances.getValue(current) + graph.edgeWeight(current, neighbor, pathHistory)
                    if (newDistance < distances.getValue(neighbor)) {
                        distances[neighbor] = newDistance
                        previous[neighbor] = current
                    }
                }
            }
        }

        // Reconstruct path
        return reconstructPath(previous, start, end)
    }

    /**
     * Helper function to reconstruct the path from start to end using the 'previous' map.
     * @param previous Map of previous vertices in the path.
     * @param start The starting vertex.
     * @param end The ending vertex.
     * @return List representing the path from start to end.
     */
    private fun reconstructPath(previous: Map<T, T?>, start: T, end: T): List<T> {
        val path = mutableListOf<T>()
        var current: T? = end
        while (current != null && current != start) {
            path.add(current)
            current = previous[current]
        }
        if (current == start) {
            path.add(start)
            return path.reversed()
        }
        return emptyList() // No path if we didn't reach the start
    }
}