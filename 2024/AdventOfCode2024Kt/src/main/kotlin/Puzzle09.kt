package de.pichlerj

import de.pichlerj.base.Puzzle
import java.lang.Integer.min

class Puzzle09 : Puzzle<MutableList<Int>, Long>(9, 2024) {
    override fun getTestData(): String {
        return "2333133121414131402"
    }

    override fun parse(input: String): MutableList<Int> {
        val array = mutableListOf<Int>()
        var ctr = 0
        for (i in input.indices) {
            val value = input[i].toString().toInt()
            if (i % 2 != 0) {
                for (j in 0 until value) {
                    array.add(-1)
                }
            } else {
                for (j in 0 until value) {
                    array.add(ctr)
                }
                ctr++
            }
        }
        return array
    }

    override fun solvePart02(input: MutableList<Int>): Long {
        defrag02(input)
        return checksum(input)
    }

    override fun solvePart01(input: MutableList<Int>): Long {
        defrag01(input)
        return checksum(input)
    }

    private fun defrag01(array: MutableList<Int>) {
        var indexFreeSpace = array.indexOf(-1)
        var indexData = array.size - 1
        assert(array[indexData] != -1)
        while (indexFreeSpace < indexData) {

            array[indexFreeSpace] = array[indexData]
            array[indexData] = -1

            while (array[indexFreeSpace] != -1) {
                indexFreeSpace++
            }
            while (array[indexData] == -1) {
                indexData--
            }
        }
    }

    private fun defrag02(array: MutableList<Int>) {
        val blocks = getFileBlocks(array)
        var freeSpaces = getFreeSpaces(array)

        while (blocks.size > 0) {
            val block = blocks.removeFirst()
            val maxFreeSpace = freeSpaces.keys.max()

            if(maxFreeSpace < block.length) {
                continue
            }

            var freeSpaceIndex: Int? = null
            for (i in block.length..maxFreeSpace) {
                val indicesWithFreeSpace = freeSpaces.get(i)
                if (indicesWithFreeSpace != null) {
                    if(freeSpaceIndex == null) {
                        freeSpaceIndex = indicesWithFreeSpace[0]
                    } else {
                        freeSpaceIndex = min(freeSpaceIndex, indicesWithFreeSpace[0])
                    }
                }
            }

            if (freeSpaceIndex == null || freeSpaceIndex > block.index) {
                continue
            }

            // remove block from array
            for (i in block.index until block.index + block.length) {
                array[i] = -1
            }
            // add block to new location
            for (i in freeSpaceIndex until freeSpaceIndex + block.length) {
                assert(array[i] == -1)
                array[i] = block.id
            }
            //debugPrint(array)
            freeSpaces = getFreeSpaces(array)
        }
    }

    private fun debugPrint(array: MutableList<Int>) {
        for(num in array) {
            if(num == -1){
                print('.')
            } else {
                print(num)
            }
        }
        println()
    }

    private fun getFileBlocks(array: List<Int>): MutableList<FileBlock> {
        val blocks = mutableListOf<FileBlock>()
        var ctr = array.size - 1
        while (ctr >= 0) {
            val id = array[ctr]
            if (id == -1) {
                ctr--
                continue
            }
            val lastIndex = ctr
            while (ctr >= 0 && array[ctr] == id) {
                ctr--
            }
            val firstIndex = ctr + 1
            assert(array[firstIndex] == id)
            assert(firstIndex > 0 && array[firstIndex-1] != id)
            assert(array[lastIndex] == id)
            assert(lastIndex == array.size- 1 || array[lastIndex+1] != id)
            val length = lastIndex - firstIndex + 1
            blocks.add(FileBlock(id, firstIndex, length))
        }
        return blocks
    }

    private fun getFreeSpaces(array: List<Int>): HashMap<Int, MutableList<Int>> {
        val freeSpaces = HashMap<Int, MutableList<Int>>() // map number of free blocks to starting indices
        var ctr = 0
        while (ctr < array.size) {
            if (array[ctr] != -1) {
                ctr++
                continue
            }
            val index = ctr
            while (ctr < array.size && array[ctr] == -1) {
                ctr++
            }
            val length = ctr - index
            freeSpaces.getOrPut(length, { mutableListOf() }).add(index)
        }
        return freeSpaces
    }

    private fun checksum(array: List<Int>): Long {
        var sum: Long = 0
        for (i in array.indices) {
            val value = array[i]
            if (value == -1) {
                continue
            }
            sum += (value * i)
        }
        return sum
    }
}

data class FileBlock(val id: Int, val index: Int, val length: Int)