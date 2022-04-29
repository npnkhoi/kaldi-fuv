from tracemalloc import start
from typing import List

VN2TELEX = {
  "một": "mootj",
  "hai": "hai",
  "ba": "ba",
  "bốn": "boons",
  "năm": "nawm",
  "sáu": "saus",
  "bảy": "bayr",
  "tám": "tams",
  "chín": "chins",
  "mười": "muowif",
  "mươi": "muowi",
  "lẻ": "ler",
  "mốt": "moots",
  "trăm": "trawm",
  "lăm": "lawm",
  "sil": "sil",
  "silence": "sil",
}

def get_words_from_textgrid(filename: str) -> List:
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      lines = f.readlines()
  except:
    with open(filename, 'r', encoding='utf-16-be') as f:
      lines = f.readlines()

  # print(lines)
  # print(lines[13])
  num_words = int(lines[13].split()[-1])
  ret = []
  for i in range(num_words):
    start_line = 14 + 4 * i
    xmin = float(lines[start_line + 1].split(' = ')[-1])
    xmax = float(lines[start_line + 2].split(' = ')[-1])
    # print('text line:', lines[start_line: start_line + 4])
    text = lines[start_line + 3].split(' = ')[-1].strip().strip('"')
    ret.append((xmin, xmax, text))
  return ret