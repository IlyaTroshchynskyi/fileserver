import file_service
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="""Work with files. Has four functions:read_file:[-nm],create_file:[-ln,-ext,-con,
        -lt,dg],delete_file:[-nm],get_metadata_file:[-nm]""")

    parser.add_argument('-nm', '--name', help='Enter name of file')
    parser.add_argument('-ln', '--length', type=int, help='Enter the length for your file name ')
    parser.add_argument('-ext', '--extension', choices=['.txt', '.py', '.xml', '.css', '.html'],
                        help='Enter extension of your file')
    parser.add_argument('-con', '--content', help='Enter content for your file')
    parser.add_argument('-lt', '--letters', type=int, choices=[0, 1], help='Do you want to create file'
                                                                           'name with helping letters?')
    parser.add_argument('-dg', '--digits', type=int, choices=[0, 1], help='Do you want to create file'
                                                                          'name with helping digits?')
    parser.add_argument('-a', '--action', required=True, help="Choose function for working with files")

    args = parser.parse_args()

    if args.action == 'read_file':
        file_service.read_file(args.name)
    elif args.action == 'create_file':
        file_service.create_file(length_name=args.length, extension=args.extension, content=args.content,
                                 letters=bool(args.letters), digit=bool(args.digits))
    elif args.action == 'delete_file':
        file_service.delete_file(args.name)
    elif args.action == 'get_metadata_file':
        file_service.get_metadata_file(args.name)
    else:
        print('Try again you choose wrong command')