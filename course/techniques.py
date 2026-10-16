"""Every technique a problem may rely on. Each one is taught by exactly one basic problem (the one
that lists it in TEACHES), earlier in the course than any problem that lists it in USES.
`python server.py --check coverage` enforces this. Explanations: 2-4 sentences, inline `code` allowed."""

TECHNIQUES = {
    "grid.neighbors": {
        "name": "Grid neighbours",
        "explain": "A cell (r, c) has up to four neighbours: (r - 1, c), (r + 1, c), (r, c - 1) and (r, c + 1). "
                   "Check `0 <= nr < rows and 0 <= nc < cols` before you look at one, and skip walls.",
    },
    "bfs.shortest": {
        "name": "BFS for fewest steps",
        "explain": "Put the start in a queue at distance 0. Pop a cell and give each unvisited neighbour distance + 1 "
                   "before queueing it. The queue hands out cells in order of distance, so the first time you reach "
                   "a cell is along a shortest path.",
    },
    "bfs.multi_source": {
        "name": "Multi-source BFS",
        "explain": "When there are several starts, put all of them in the queue at distance 0 before the loop. The "
                   "search then spreads from every start at once, and each cell gets its distance to the nearest start.",
    },
    "dfs.flood_fill": {
        "name": "Flood fill",
        "explain": "From one cell, visit every connected cell that matches (same colour, open floor), marking each "
                   "one as you reach it so it's never visited twice. A stack (DFS) or a queue (BFS) both cover the "
                   "whole region.",
    },
    "graph.components": {
        "name": "Counting connected regions",
        "explain": "Scan every cell (or node). Each time you find one you haven't visited, that's a new region: "
                   "count it, then flood fill the whole region so none of its cells starts a region again.",
    },
    "graph.adjacency": {
        "name": "Walking a graph from its edges",
        "explain": "When a graph comes as a list of edges, first build an adjacency list: for an undirected edge "
                   "(a, b), add b to a's list and a to b's. Then BFS or DFS with a `seen` set. The same walk works "
                   "when nodes link to their neighbours directly, like `node.neighbors`.",
    },
    "flood.from_targets": {
        "name": "Searching back from the targets",
        "explain": 'Instead of asking "can this cell reach the edge?" once per cell, search once FROM the targets '
                   "(often the border cells) and mark everything they reach. One flood from many starts replaces "
                   "one search per cell.",
    },
    "bfs.implicit": {
        "name": "BFS with generated neighbours",
        "explain": "Sometimes nobody lists the neighbours: you work them out from the current state, such as a "
                   "number's x + 1, x - 1 and x * 2, or a word with one letter changed. Generate them inside the "
                   "BFS loop and keep a `seen` set of states.",
    },
    "bfs.state": {
        "name": "BFS over a richer state",
        "explain": "When the same cell can matter twice (before and after picking up a key, say), put the extra "
                   "information into the state: (row, col, has_key). The `seen` set holds whole states, so you "
                   "may stand on a cell once per state.",
    },
    "bfs.path": {
        "name": "Rebuilding the path",
        "explain": "BFS finds distances, not routes. Record each cell's parent (the cell you reached it from) the "
                   "first time you see it. When you reach the goal, follow the parents back to the start and reverse.",
    },
}
