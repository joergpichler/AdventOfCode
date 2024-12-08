package de.pichlerj.utils

data class Vector(val dx: Int, val dy: Int){
    fun invert(): Vector {
        return Vector(-dx, -dy)
    }

    fun multiply(scalar: Int): Vector {
        return Vector(dx * scalar, dy * scalar)
    }
}