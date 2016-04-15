import shell
import walkinput

def main():
    config = shell.get_config()
    print config

    print walkinput.headers(config)
    print walkinput.sources(config)


if __name__ == '__main__':
    main()
