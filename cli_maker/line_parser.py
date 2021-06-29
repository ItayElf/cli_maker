def parse_line(argv):
    regular = []
    arguments = {}
    flags = {}
    if len(argv) == 0:
        return None

    if len(argv) == 1:
        return argv[0], regular, arguments, flags

    i = 1
    while i <= len(argv)-1 and not argv[i].startswith("-"):
        regular.append(argv[i])
        i += 1
    
    while i <= len(argv)-1 and not argv[i].startswith("--"):
        try:
            arguments[argv[i][1:]] = argv[i+1]
            i += 2
        except IndexError:
            raise Exception(f"arg {argv[i]} has no matching value")

    while i != len(argv):
        flags[argv[i][2:]] = True
        i += 1

    return argv[0], regular, arguments, flags
    