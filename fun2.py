import os.path

from PIL import Image   # This uses Pillow, the PIL fork for Python 3.4
                        # https://pypi.python.org/pypi/Pillow

from random import random, sample, randrange, shuffle
from time import perf_counter


def make_line_picture(image_filename):
    '''Save SVG image of closed curve approximating input image.'''
    input_image_path = os.path.abspath(image_filename)
    image = Image.open(input_image_path)
    width, height = image.size
    scale = 1024 / width
    head, tail = os.path.split(input_image_path)
    output_tail = 'TSP_' + os.path.splitext(tail)[0] + '.html'
    output_filename = os.path.join(head, output_tail)
    points = generate_points(image)
    population = len(points)
    save_dither(points, image)
    grid_cells = [set() for i in range(width * height)]
    line_cells = [set() for i in range(population)]
    print('Initialising acceleration grid')
    for i in range(population):
        recalculate_cells(i, width, points, grid_cells, line_cells)
    while True:
        save_svg(output_filename, width, height, points, scale)
        improve_TSP_solution(points, width, grid_cells, line_cells)


def save_dither(points, image):
    '''Save a copy of the dithered image generated for approximation.'''
    image = image.copy()
    pixels = list(image.getdata())
    pixels = [255] * len(pixels)
    width, height = image.size
    for p in points:
        x = int(p[0])
        y = int(p[1])
        pixels[x+y*width] = 0
    image.putdata(pixels)
    image.save('dither_test.png', 'PNG')


def generate_points(image):
    '''Return a list of points approximating the image.

    All points are offset by small random amounts to prevent parallel lines.'''
    width, height = image.size
    image = image.convert('L')
    pixels = image.getdata()
    points = []
    gap = 1
    r = random
    for y in range(2*gap, height - 2*gap, gap):
        for x in range(2*gap, width - 2*gap, gap):
            if (r()+r()+r()+r()+r()+r())/6 < 1 - pixels[x + y*width]/255:
                        points.append((x + r()*0.5 - 0.25,
                                       y + r()*0.5 - 0.25))
    shuffle(points)
    print('Total number of points', len(points))
    print('Total length', current_total_length(points))
    return points


def current_total_length(points):
    '''Return the total length of the current closed curve approximation.'''
    population = len(points)
    return sum(distance(points[i], points[(i+1)%population])
               for i in range(population))


def recalculate_cells(i, width, points, grid_cells, line_cells):
    '''Recalculate the grid acceleration cells for the line from point i.'''
    for j in line_cells[i]:
        try:
            grid_cells[j].remove(i)
        except KeyError:
            print('grid_cells[j]',grid_cells[j])
            print('i',i)
    line_cells[i] = set()
    add_cells_along_line(i, width, points, grid_cells, line_cells)
    for j in line_cells[i]:
        grid_cells[j].add(i)


def add_cells_along_line(i, width, points, grid_cells, line_cells):
    '''Add each grid cell that lies on the line from point i.'''
    population = len(points)
    start_coords = points[i]
    start_x, start_y = start_coords
    end_coords = points[(i+1) % population]
    end_x, end_y = end_coords
    gradient = (end_y - start_y) / (end_x - start_x)
    y_intercept = start_y - gradient * start_x
    total_distance = distance(start_coords, end_coords)
    x_direction = end_x - start_x
    y_direction = end_y - start_y
    x, y = start_x, start_y
    grid_x, grid_y = int(x), int(y)
    grid_index = grid_x + grid_y * width
    line_cells[i].add(grid_index)
    while True:
        if x_direction > 0:
            x_line = int(x + 1)
        else:
            x_line = int(x)
            if x_line == x:
                x_line = x - 1
        if y_direction > 0:
            y_line = int(y + 1)
        else:
            y_line = int(y)
            if y_line == y:
                y_line = y - 1
        x_line_intersection = gradient * x_line + y_intercept
        y_line_intersection = (y_line - y_intercept) / gradient
        x_line_distance = distance(start_coords, (x_line, x_line_intersection))
        y_line_distance = distance(start_coords, (y_line_intersection, y_line))
        if (x_line_distance > total_distance and
            y_line_distance > total_distance):
            break
        if x_line_distance < y_line_distance:
            x = x_line
            y = gradient * x_line + y_intercept
        else:
            y = y_line
            x = (y_line - y_intercept) / gradient
        grid_x = int(x - (x_direction < 0) * (x == int(x)))
        grid_y = int(y - (y_direction < 0) * (y == int(y)))
        grid_index = grid_x + grid_y * width
        line_cells[i].add(grid_index)


def improve_TSP_solution(points, width, grid_cells, line_cells,
                         performance=[0,0,0], total_length=None):
    '''Apply 3 approaches, allocating time to each based on performance.'''
    population = len(points)
    if total_length is None:
        total_length = current_total_length(points)

    print('Swapping pairs of vertices')
    if performance[0] == max(performance):
        time_limit = 300
    else:
        time_limit = 10
    print('    Aiming for {} seconds'.format(time_limit))
    start_time = perf_counter()
    for n in range(1000000):
        swap_two_vertices(points, width, grid_cells, line_cells)
        if perf_counter() - start_time > time_limit:
            break
    time_taken = perf_counter() - start_time
    old_length = total_length
    total_length = current_total_length(points)
    performance[0] = (old_length - total_length) / time_taken
    print('    Time taken', time_taken)
    print('    Total length', total_length)
    print('    Performance', performance[0])

    print('Moving single vertices')
    if performance[1] == max(performance):
        time_limit = 300
    else:
        time_limit = 10
    print('    Aiming for {} seconds'.format(time_limit))
    start_time = perf_counter()
    for n in range(1000000):
        move_a_single_vertex(points, width, grid_cells, line_cells)
        if perf_counter() - start_time > time_limit:
            break
    time_taken = perf_counter() - start_time
    old_length = total_length
    total_length = current_total_length(points)
    performance[1] = (old_length - total_length) / time_taken
    print('    Time taken', time_taken)
    print('    Total length', total_length)
    print('    Performance', performance[1])

    print('Uncrossing lines')
    if performance[2] == max(performance):
        time_limit = 60
    else:
        time_limit = 10
    print('    Aiming for {} seconds'.format(time_limit))
    start_time = perf_counter()
    for n in range(1000000):
        uncross_lines(points, width, grid_cells, line_cells)
        if perf_counter() - start_time > time_limit:
            break
    time_taken = perf_counter() - start_time
    old_length = total_length
    total_length = current_total_length(points)
    performance[2] = (old_length - total_length) / time_taken
    print('    Time taken', time_taken)
    print('    Total length', total_length)
    print('    Performance', performance[2])


def swap_two_vertices(points, width, grid_cells, line_cells):
    '''Attempt to find a pair of vertices that reduce length when swapped.'''
    population = len(points)
    for n in range(100):
        candidates = sample(range(population), 2)
        befores = [(candidates[i] - 1) % population
                   for i in (0,1)]
        afters = [(candidates[i] + 1) % population for i in (0,1)]
        current_distance = sum((distance(points[befores[i]],
                                         points[candidates[i]]) +
                                distance(points[candidates[i]],
                                         points[afters[i]]))
                               for i in (0,1))
        (points[candidates[0]],
         points[candidates[1]]) = (points[candidates[1]],
                                   points[candidates[0]])
        befores = [(candidates[i] - 1) % population
                   for i in (0,1)]
        afters = [(candidates[i] + 1) % population for i in (0,1)]
        new_distance = sum((distance(points[befores[i]],
                                     points[candidates[i]]) +
                            distance(points[candidates[i]],
                                     points[afters[i]]))
                           for i in (0,1))
        if new_distance > current_distance:
            (points[candidates[0]],
             points[candidates[1]]) = (points[candidates[1]],
                                       points[candidates[0]])
        else:
            modified_points = tuple(set(befores + candidates))
            for k in modified_points:
                recalculate_cells(k, width, points, grid_cells, line_cells)
            return


def move_a_single_vertex(points, width, grid_cells, line_cells):
    '''Attempt to find a vertex that reduces length when moved elsewhere.'''
    for n in range(100):
        population = len(points)
        candidate = randrange(population)
        offset = randrange(2, population - 1)
        new_location = (candidate + offset) % population
        before_candidate = (candidate - 1) % population
        after_candidate = (candidate + 1) % population
        before_new_location = (new_location - 1) % population
        old_distance = (distance(points[before_candidate], points[candidate]) +
                        distance(points[candidate], points[after_candidate]) +
                        distance(points[before_new_location],
                                 points[new_location]))
        new_distance = (distance(points[before_candidate],
                                 points[after_candidate]) +
                        distance(points[before_new_location],
                                 points[candidate]) +
                        distance(points[candidate], points[new_location]))
        if new_distance <= old_distance:
            if new_location < candidate:
                points[:] = (points[:new_location] +
                             points[candidate:candidate + 1] +
                             points[new_location:candidate] +
                             points[candidate + 1:])
                for k in range(candidate - 1, new_location, -1):
                    for m in line_cells[k]:
                        grid_cells[m].remove(k)
                    line_cells[k] = line_cells[k - 1]
                    for m in line_cells[k]:
                        grid_cells[m].add(k)
                for k in ((new_location - 1) % population,
                          new_location, candidate):
                    recalculate_cells(k, width, points, grid_cells, line_cells)
            else:
                points[:] = (points[:candidate] +
                             points[candidate + 1:new_location] +
                             points[candidate:candidate + 1] +
                             points[new_location:])
                for k in range(candidate, new_location - 3):
                    for m in line_cells[k]:
                        grid_cells[m].remove(k)
                    line_cells[k] = line_cells[k + 1]
                    for m in line_cells[k]:
                        grid_cells[m].add(k)
                for k in ((candidate - 1) % population,
                          new_location - 2, new_location - 1):
                    recalculate_cells(k, width, points, grid_cells, line_cells)
            return


def uncross_lines(points, width, grid_cells, line_cells):
    '''Attempt to find lines that are crossed, and reverse path to uncross.'''
    population = len(points)
    for n in range(100):
        i = randrange(population)
        start_1 = points[i]
        end_1 = points[(i + 1) % population]
        if not line_cells[i]:
            recalculate_cells(i, width, points, grid_cells, line_cells)
        for cell in line_cells[i]:
            for j in grid_cells[cell]:
                if i != j and i != (j+1)%population and i != (j-1)%population:
                    start_2 = points[j]
                    end_2 = points[(j + 1) % population]
                    if are_crossed(start_1, end_1, start_2, end_2):
                        if i < j:
                            points[i + 1:j + 1] = reversed(points[i + 1:j + 1])
                            for k in range(i, j + 1):
                                recalculate_cells(k, width, points, grid_cells,
                                                  line_cells)
                        else:
                            points[j + 1:i + 1] = reversed(points[j + 1:i + 1])
                            for k in range(j, i + 1):
                                recalculate_cells(k, width, points, grid_cells,
                                                  line_cells)
                        return


def are_crossed(start_1, end_1, start_2, end_2):
    '''Return True if the two lines intersect.'''
    if end_1[0]-start_1[0] and end_2[0]-start_2[0]:
        gradient_1 = (end_1[1]-start_1[1])/(end_1[0]-start_1[0])
        gradient_2 = (end_2[1]-start_2[1])/(end_2[0]-start_2[0])
        if gradient_1-gradient_2:
            intercept_1 = start_1[1] - gradient_1 * start_1[0]
            intercept_2 = start_2[1] - gradient_2 * start_2[0]
            x = (intercept_2 - intercept_1) / (gradient_1 - gradient_2)
            if (x-start_1[0]) * (end_1[0]-x) > 0 and (x-start_2[0]) * (end_2[0]-x) > 0:
                return True


def distance(point_1, point_2):
    '''Return the Euclidean distance between the two points.'''
    return sum((point_1[i] - point_2[i]) ** 2 for i in (0, 1)) ** 0.5


def save_svg(filename, width, height, points, scale):
    '''Save a file containing an SVG path of the points.'''
    print('Saving partial solution\n')
    with open(filename, 'w') as file:
        file.write(content(width, height, points, scale))


def content(width, height, points, scale):
    '''Return the full content to be written to the SVG file.'''
    return (header(width, height, scale) +
            specifics(points, scale) +
            footer()
            )


def header(width, height,scale):
    '''Return the text of the SVG header.'''
    return ('<?xml version="1.0"?>\n'
            '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN"\n'
            '    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n'
            '\n'
            '<svg width="{0}" height="{1}">\n'
            '<title>Traveling Salesman Problem</title>\n'
            '<desc>An approximate solution to the Traveling Salesman Problem</desc>\n'
            ).format(scale*width, scale*height)


def specifics(points, scale):
    '''Return text for the SVG path command.'''
    population = len(points)
    x1, y1 = points[-1]
    x2, y2 = points[0]
    x_mid, y_mid = (x1 + x2) / 2, (y1 + y2) / 2
    text = '<path d="M{},{} L{},{} '.format(x1, y1, x2, y2)
    for i in range(1, population):
        text += 'L{},{} '.format(*points[i])
    text += '" stroke="black" fill="none" stroke-linecap="round" transform="scale({0},{0})" vector-effect="non-scaling-stroke" stroke-width="3"/>'.format(scale)
    return text


def footer():
    '''Return the closing text of the SVG file.'''
    return '\n</svg>\n'


if __name__ == '__main__':
    import sys
    arguments = sys.argv[1:]
    if arguments:
        make_line_picture(arguments[0])
    else:
        print('Required argument: image file')
