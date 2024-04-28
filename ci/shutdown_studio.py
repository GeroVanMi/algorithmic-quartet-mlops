from studio_helper import create_studio


def shutdown_studio():
    studio = create_studio()
    print("Shutting studio down.")
    studio.stop()


if __name__ == "__main__":
    shutdown_studio()
