from pathlib import Path
from rembg import remove, new_session

session = new_session()

for file in Path('/Users/yichao/Desktop').glob('*.png'):
    input_path = str(file)
    output_path = str(file.parent / (file.stem + ".out.png"))
    print(input_path)
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input, session=session)
            o.write(output)
