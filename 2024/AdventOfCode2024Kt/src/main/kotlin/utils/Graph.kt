package de.pichlerj.utils

interface Graph<T> {
    /**
     * Returns a list of all vertices in the graph.
     */
    fun vertices(): List<T>

    /**
     * Returns a list of adjacent vertices to the given vertex.
     * @param vertex The vertex to find adjacents for.
     * @return List of adjacent vertices.
     */
    fun adjacents(vertex: T): List<T>

    /**
     * Returns the weight of the edge between two vertices considering the path history.
     * @param from The starting vertex.
     * @param to The ending vertex.
     * @param pathHistory The list of vertices already visited in the path.
     * @return The weight of the edge or Double.POSITIVE_INFINITY if no edge exists.
     */
    fun edgeWeight(from: T, to: T, pathHistory: List<T>): Double
}