# mode: compile

# This caused a "maximum recursion depth exceeded" at some point,
# see https://github.com/cython/cython/issues/1744

cdef inline bint g(int x, int y): return True

cdef cython_bug(int u):
    try:
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
        g(u, u)
    finally:
        g(u, u)

cython_bug(1)
