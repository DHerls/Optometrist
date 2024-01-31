from src.generators.grid import create_grid, XYPair, GridOptions, fill_grid_cell

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grid_size", type=int)
    parser.add_argument("cell_size", type=int)
    parser.add_argument("--padding", type=int, default=5)
    parser.add_argument("--line-width", type=int, default=1)
    parser.add_argument("--coords", choices=["alpha", "num", "alphanum", "numalpha"])
    parser.add_argument("--fill", help="x,y grid coord to color")

    args = parser.parse_args()

    options = GridOptions(grid_size=(args.grid_size, args.grid_size), cell_size=(args.cell_size, args.cell_size), padding=args.padding, line_width=args.line_width, coords_type=args.coords)

    img = create_grid(options)

    if "fill" in args:
        fill_grid_cell(options, img, (4, 4), (255, 0, 0))

    img.save("grid.png", format="PNG")


if __name__ == "__main__":
    main()
