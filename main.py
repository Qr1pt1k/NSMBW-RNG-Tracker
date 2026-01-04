# main.py

import sys

from interface import AnyPercentUI

def main() -> int:
    ui = AnyPercentUI()
    ui.mainloop()

    return 0

if __name__ == '__main__':
    sys.exit(main())
