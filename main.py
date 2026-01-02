
# main.py

import os
import sys

from interface import AnyPercentInterface

def main() -> int:
    gui = AnyPercentInterface()
    gui.mainloop()

    return 0

if __name__ == '__main__':
    sys.exit(main())
