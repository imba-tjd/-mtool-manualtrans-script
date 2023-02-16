import json
import typing

TranslateService = typing.Callable[[str], str]

EnablePrint = True


def process(data: dict[str, str], translator: TranslateService):
    total = len(data)
    count = 0

    for key, value in data.items():
        if key != value:  # treat as translated
            count += 1
            continue

        try:
            translated = translator(value)
        except Exception:
            print('Failed to translate %s' % value)
            raise

        if EnablePrint:
            count += 1
            print('\rTranslated %d/%d %d%%' % (count, total, count/total*100), end='')

        data[key] = translated


def process_file(translator: TranslateService, filename='ManualTransFile.json'):
    with open(filename, encoding='u8') as f:
        data = json.load(f)

    try:
        process(data, translator)
    finally:
        with open(filename, 'w', encoding='u8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def data2lines(data: dict[str, str]):
    for key in data:
        yield key


def lines2data(lines: typing.Iterable[str], data: dict[str, str]):
    for key, value in zip(data, lines):
        data[key] = value


def file2lines(filename='ManualTransFile.json'):
    with open(filename, encoding='u8') as f:
        data = json.load(f)

    with open('ManualTransLines.txt', 'w', encoding='u8') as f:
        for line in data2lines(data):
            f.write(line + '\n')
