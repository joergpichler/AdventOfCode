package de.pichlerj

import de.pichlerj.base.Puzzle

class Puzzle05 : Puzzle<Puzzle05Data, Int>(5, 2024) {
    override fun getTestData(): String {
        return "47|53\n" +
                "97|13\n" +
                "97|61\n" +
                "97|47\n" +
                "75|29\n" +
                "61|13\n" +
                "75|53\n" +
                "29|13\n" +
                "97|29\n" +
                "53|29\n" +
                "61|53\n" +
                "97|53\n" +
                "61|29\n" +
                "47|13\n" +
                "75|47\n" +
                "97|75\n" +
                "47|61\n" +
                "75|61\n" +
                "47|29\n" +
                "75|13\n" +
                "53|13\n" +
                "\n" +
                "75,47,61,53,29\n" +
                "97,61,53,29,13\n" +
                "75,29,13\n" +
                "75,97,47,61,53\n" +
                "61,13,29\n" +
                "97,13,75,29,47"
    }

    override fun parse(input: String): Puzzle05Data {
        val orderingRules = mutableListOf<OrderingRule>()
        val pageUpdates = mutableListOf<PageUpdate>()
        var parsePt2 = false
        for (line in input.lines()) {
            if (line.isBlank()) {
                parsePt2 = true
                continue
            }
            if (!parsePt2) {
                line.split('|').let { parts ->
                    val page1 = parts[0].toInt()
                    val page2 = parts[1].toInt()
                    orderingRules.add(OrderingRule(page1, page2))
                }
            } else {
                line.split(',').let { parts ->
                    val pages = parts.map { it.toInt() }
                    pageUpdates.add(PageUpdate(pages))
                }
            }
        }
        return Puzzle05Data(orderingRules, pageUpdates)
    }

    override fun solvePart02(input: Puzzle05Data): Int {
        var result = 0
        for (pageUpdate in input.pageUpdates) {
            if (!isValid(pageUpdate, input.orderingRules)) {
                val orderedPages = pageUpdate.getInOrder(input.orderingRules)
                val index = orderedPages.size / 2
                result += orderedPages[index]
            }
        }
        return result
    }

    override fun solvePart01(input: Puzzle05Data): Int {
        var result = 0
        for (pageUpdate in input.pageUpdates) {
            if (isValid(pageUpdate, input.orderingRules)) {
                val index = pageUpdate.pages.size / 2
                result += pageUpdate.pages[index]
            }
        }
        return result
    }

    private fun isValid(pageUpdate: PageUpdate, orderingRules: List<OrderingRule>): Boolean {
        val printedPages = mutableListOf<Int>()
        for (page in pageUpdate.pages) {
            printedPages.add(page)
            if (!orderingRules.all { it.appliesTo(printedPages) }) {
                return false
            }
        }
        return true
    }
}

data class Puzzle05Data(val orderingRules: List<OrderingRule>, val pageUpdates: List<PageUpdate>)

class OrderingRule(val page1: Int, val page2: Int) {
    fun appliesTo(printedPages: List<Int>): Boolean {
        val index1 = printedPages.indexOf(page1)
        val index2 = printedPages.indexOf(page2)
        return index1 == -1 || index2 == -1 || index1 < index2
    }
}

class PageUpdate(val pages: List<Int>) {
    fun getInOrder(orderingRules: List<OrderingRule>): List<Int> {
        val newPages = pages.toMutableList()
        while (true) {
            var ruleApplied = false

            for (rule in orderingRules) {
                val index1 = newPages.indexOf(rule.page1)
                val index2 = newPages.indexOf(rule.page2)
                if (index1 != -1 && index2 != -1 && index1 > index2) {
                    newPages[index1] = rule.page2
                    newPages[index2] = rule.page1
                    ruleApplied = true
                }
            }

            if (!ruleApplied) {
                break
            }
        }
        return newPages
    }
}