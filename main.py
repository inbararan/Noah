import reader
from writers import csvfy, hazanotomat
from identify import report_uuid_errors


def main():
    option = input("What do you want to do?"
                   "\t1 for the Hazanot-O-mat"
                   "\t2 for a CSV of all data\n")
    write = {
        '1': hazanotomat.write,
        '2': csvfy.write
    }.get(option) or exit(0)

    write(reader.read())
    
    report_uuid_errors()
    print("Done")


if __name__ == '__main__':
    main()
