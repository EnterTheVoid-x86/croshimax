import kernel.filesystem

desc = "Returns the contents of a directory."
parser = kernel.filesystem.Parser('ls', name="List Directory", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-l', action="store_true", dest="long", default=False)
pa('-a', action="store_true", dest="all", default=False)

def run(shell, args):
    fscp = kernel.filesystem.calc_permission_string
    fsgm = kernel.filesystem.get_meta_data
    fsbn = kernel.filesystem.base_name
    format = "%s %s %s %s"

    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            paths = args.paths
        else:
            paths = [shell.path]
        for relpath in paths:
            path = shell.sabs_path(relpath)
            try:
                a = kernel.filesystem.list_dir(path)
                if args.long:
                    b = [fsgm(shell.sabs_path(kernel.filesystem.join_path(path, x))) for x in a]
                    a = [format % (fscp(perm), owner, "1", fsbn(name)) for name, owner, perm in b]

                if len(paths) > 1:
                    shell.stdout.write("%s:" % (relpath, ))
                if shell.stdout or args.long:
                    shell.stdout.write('\n'.join(a))
                    shell.stdout.write('')  # end with newline
                else:
                    maxlen = max([len(x) for x in a])
                    # arbitrary line length
                    columns = (80 / maxlen) - 1
                    shell.stdout.write('')  # skip <out> line
                    b = []
                    for i, x in enumerate(a):
                        newline = "\n" if not ((i + 1) % columns) else ""
                        if not ((i + 1) % columns):
                            newline = "\n"
                            spacing = ""
                        else:
                            newline = ""
                            spacing = " " * (maxlen - len(x) + 1)
                        b.append(x + spacing + newline)
                    shell.stdout.write(''.join(b).rstrip())
                    shell.stdout.write('')  # end with newline
            except OSError:
                shell.stderr.write('ls: cannot acces %s: no such file or directory\n' % (relpath, ))


def help():
    return parser.help_msg()
