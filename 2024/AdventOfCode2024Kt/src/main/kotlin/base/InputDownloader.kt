package de.pichlerj.base

import java.net.HttpURLConnection
import java.net.URI

class InputDownloader {
    fun download(day: Int, year: Int): String {
        val url = URI.create("https://adventofcode.com/$year/day/$day/input").toURL()
        val connection = url.openConnection() as HttpURLConnection
        connection.setRequestProperty("Cookie", "session=${SESSION}")

        connection.inputStream.bufferedReader().use {
            val content = it.readText()
            return content
        }
    }
}