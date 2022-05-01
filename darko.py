import darko.interpreter

if __name__ == '__main__':

    transf_src = {
        'negative':
        'new[x, y] = Z - old[x, y]',
        'mirror':
        'new[x, y] = old[X - x, y]',
        'bath':
        'new[x, y] = old[x + (x % 32) - 16, y]',
        'bentley':
        'new[x, y - gray(old[x, y]) * 0.1] = old[x, y]',
        'upright':
        'new[x, y] = old[rect(r, a + rad(180))]',
        'twist':
        'new[x, y] = old[rect(r, a - r / 50)]',
        'fisheye':
        'new[x, y] = old[rect(1.5 * r ** 2 / R, a)]',
        'caricature':
        'new[x, y] = old[rect(0.5 * sqrt(r * R), a)]',
        'funhouse':
        'new[x, y] = old[x + sin(rad(x)) * 150, y + sin(rad(y * 1.18)) * 89]',
        'spiralbath':
        'new[x, y] = old[x, y + (deg(a) + r / 4) % 64 - 16]',
        'pond':
        'new[x, y] = old[x, y + 10 * sin(rad(y) * 10)]',
        'curly':
        'new[x, y] = old[x + 10 * sin(rad(y) * 5), y + 10 * sin(rad(x) * 5)]',
        'wave':
        'new[x, y] = old[x + 10 * sin(rad(y) * 10), y]',
        'sink':
        'new[x, y] = old[rect(r + 10 * sin(rad(r) * 10), a - r / 50)]',
        't2000':
        'new[x, y] = old[rect(1.5 * r ** 2 / R + 10 * sin(rad(r) * 10), a)]',
        'pixel':
        'new[x, y] = old[floor(x / 10) * 10, floor(y / 10) * 10]',
    }

    pairs = [('twist', 'putin'), ('bath', 'merkel'),
             ('wave', 'obama'), ('pond', 'cameron'),
             ('fisheye', 'bezos'), ('caricature', 'page'),
             ('spiralbath', 'gates'), ('sink', 'ma'),
             ('t2000', 'zuckerberg'), ('pixel', 'musk'),
             ('bentley', 'nadella'), ('negative', 'cook'),
             ('curly', 'brin'), ('funhouse', 'jinping')]

    darko_interpreter = darko.interpreter.Interpreter()

    for pair in pairs:
        oldfilename = "docs/images/catalogue/" + pair[1] + '.jpg'
        newfilename = "./" + pair[1] + '-' + pair[0] + '.jpg'

        print(pair[0] + ": " + transf_src[pair[0]] + " -> " + newfilename)

        darko_interpreter.load(oldfilename, sampling='bilinear')
        darko_interpreter.eval(transf_src[pair[0]])
        darko_interpreter.save(newfilename, 'new')
