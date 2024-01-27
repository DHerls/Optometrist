from dataclasses import dataclass

from PIL import Image, ImageDraw

XYPair = tuple[int, int]


@dataclass
class XYPair:
    x: int
    y: int

@dataclass
class GridOptions:
    """
    cell_size: number of pixels within the borders of each cell

    padding: number of pixels outside the border of the grid on each side
    """
    cell_size: XYPair
    grid_size: XYPair
    padding = 5
    line_width = 1


def create_grid(options: GridOptions) -> Image.Image:
    cell_size_x, cell_size_y = options.cell_size
    num_cells_x, num_cells_y = options.grid_size

    image_width = side_length(cell_size_x, num_cells_x, options.padding, options.line_width)
    image_height = side_length(cell_size_y, num_cells_y, options.padding, options.line_width)

    img = Image.new("RGB", (image_width, image_height), (255, 255, 255))

    draw = ImageDraw.Draw(img)

    # Vertical Lines
    min_y = options.padding
    max_y = image_height - options.padding - 1
    for line_number in range(num_cells_x + 1):
        min_x = options.padding + (line_number * (cell_size_x + options.line_width))
        max_x = min_x + options.line_width - 1
        draw.rectangle([(min_x, min_y), (max_x, max_y)], (0, 0, 0))
    
    # Horizontal Lines
    min_x = options.padding
    max_x = image_width - options.padding - 1
    for line_number in range(num_cells_y + 1):
        min_y = options.padding + (line_number * (cell_size_y + options.line_width))
        max_y = min_y + options.line_width - 1
        draw.rectangle([(min_x, min_y), (max_x, max_y)], (0, 0, 0))

    return img


def fill_grid_cell(options: GridOptions, grid: Image.Image, coordinates: XYPair, fill: tuple[int, int, int], padding=1):
    coord_x, coord_y = coordinates
    if coord_x >= options.grid_size[0] or coord_y >= options.grid_size[1]:
        raise Exception(f"Grid coordinates {coordinates} outside grid size {options.grid_size}")

    draw = ImageDraw.Draw(grid)

    min_x = grid_cell_start(coord_x, options.cell_size[0], options.padding, options.line_width) + padding
    min_y = grid_cell_start(coord_y, options.cell_size[1], options.padding, options.line_width) + padding

    max_x = min_x + options.cell_size[0] - (2 * padding) - 1
    max_y = min_y + options.cell_size[1] - (2 * padding) - 1

    draw.rectangle([(min_x, min_y), (max_x, max_y)], fill)



def grid_cell_start(coord: int, cell_size: int, padding: int, line_width: int) -> int:
    return padding + (line_width * (coord + 1)) + coord * cell_size


def side_length(cell_size: int, num_cells: int, padding: int, line_width: int) -> int:
    return cell_size * num_cells + padding * 2 + line_width * (num_cells + 1)