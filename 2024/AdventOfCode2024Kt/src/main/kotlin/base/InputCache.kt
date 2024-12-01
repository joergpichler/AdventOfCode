package de.pichlerj.base

import java.nio.file.Path
import kotlin.io.path.*

class InputCache(cacheDir: String) {

    private val path: Path = Path(cacheDir)
    private val downloader = InputDownloader()

    init {
        require(path.exists() && path.isDirectory()) {
            "Cache directory does not exist or is not a directory: $cacheDir"
        }
    }

    fun getInput(day: Int, year: Int): String {
        val path = getPath(day, year)
        val input: String
        if (!path.exists()) {
            input = downloader.download(day, year)
            if(!path.parent.exists()){
                path.parent.createDirectory()
            }
            path.writeText(input)
        } else {
            input = path.readText()
        }
        return input
    }

    private fun getPath(day: Int, year: Int): Path {
        return path.resolve("$year/${day.toString().padStart(2, '0')}.txt")
    }
}