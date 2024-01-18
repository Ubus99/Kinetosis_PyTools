import csv
import random
import time
import tkinter.filedialog


def genTimeVal(columns: int, rows: int, int_from: int, int_to: int) -> list:
    out = []
    for r in range(rows):
        row = [time.time()]
        for c in range(columns):
            row.append(random.randrange(int_from, int_to))
        out.append(row)
    return out


def genEnumVal(columns: int, rows: int, int_from: int, int_to: int) -> list:
    out = []
    for r in range(rows):
        row = [input("name of row" + str(r) + ":\n")]
        for c in range(columns):
            row.append(random.randrange(int_from, int_to))
        out.append(row)
    return out


def genNumVal(columns: int, rows: int, int_from: int, int_to: int) -> list:
    out = []
    for r in range(rows):
        row = [str(r)]
        for c in range(columns):
            row.append(random.randrange(int_from, int_to))
        out.append(row)
    return out


def main():
    file_path = tkinter.filedialog.asksaveasfilename(filetypes=[("CSV", "*.csv; *.CSV")])
    with open(file_path, mode="w", newline="") as f:
        spamwriter = csv.writer(f, delimiter=";")

        c = int(input("number of columns:\n"))
        r = int(input("size of dataset:\n"))
        t = input("type of dataset: [realtime, list, enum]\n")
        i_f = int(input("from:\n"))
        i_t = int(input("to:\n"))
        header = [""]
        for i in range(c):
            header.append("p" + str(i + 1))
        spamwriter.writerow(header)

        match t:
            case "realtime":
                data = genTimeVal(c, r, i_f, i_t)
            case "enum":
                data = genEnumVal(c, r, i_f, i_t)
            case "list":
                data = genNumVal(c, r, i_f, i_t)
            case _:
                print("error, invalid type")
        spamwriter.writerows(data)
    print("file successfully generated!")


if __name__ == "__main__":
    main()
