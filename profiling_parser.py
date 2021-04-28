import pstats

if __name__ == "__main__":
    p = pstats.Stats("profiling/profiling_stats-2021-03-20 16-50-14.576841.stat")
    p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
