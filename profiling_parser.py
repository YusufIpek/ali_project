import pstats

if __name__ == "__main__":
    p = pstats.Stats(
        'profiling/profiling_stats-2021-03-20 12-01-35.686262.stat')
    p.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
