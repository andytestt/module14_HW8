from models import Qoute

qoutes = Qoute.objects()


def find_by_name(value):
    finding_qoutes = []
    full_name = value.split(":")[1]
    for qoute in qoutes:
        if qoute.author.fullname.lower() == full_name.lower():
            finding_qoutes.append(qoute.qoute)
    print(finding_qoutes)


def find_by_tag(value):
    finding_qoutes = []
    tags = value.split(":")[1].split(",")
    for qoute in qoutes:
        for tag in tags:
            if tag in qoute.tags:
                finding_qoutes.append(qoute.qoute)
    print(finding_qoutes)


while True:
    command = input("Enter command like 'command:value': ")

    if command.startswith("name"):
        find_by_name(command)
    elif command.startswith("tag") or command.startswith("tags"):
        find_by_tag(command)
    elif command.startswith("exit"):
        break
    else:
        continue