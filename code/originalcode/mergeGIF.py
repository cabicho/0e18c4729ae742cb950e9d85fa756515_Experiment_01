import imageio, sys

def main():
    if len(sys.argv) < 4:
        print("Usage:\nmergeGIF.py <FIRST-FRAME> [<MIDDLE-FRAME>] <LAST-FRAME> <OUTPUT-FILE>")
    elif len(sys.argv) == 4:
        first_frame = imageio.imread(sys.argv[1])
        second_frame = imageio.imread(sys.argv[2])

        images = []
        for i in range(500):
            images.append(first_frame)
        images.append(second_frame)
        imageio.mimsave(sys.argv[3], images, format='GIF', duration=1)
    else:
        first_frame = imageio.imread(sys.argv[1])
        middle_frame = imageio.imread(sys.argv[2])
        second_frame = imageio.imread(sys.argv[3])

        images = []
        images.append(first_frame)
        for i in range(500):
            images.append(middle_frame)
        images.append(second_frame)
        imageio.mimsave(sys.argv[4], images, format='GIF', duration=1)

if __name__ == "__main__":
    main()