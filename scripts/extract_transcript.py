# -*- coding: utf-8 -*-
"""会议录音文字版 → 纯文本校对底稿。
支持 .doc / .docx / .pdf / .txt / .md，按扩展名自动选解码方式。
用法:
  python extract_transcript.py --input <文件> --out <输出txt>
"""
import argparse
import os
import re
import zipfile


def extract_doc(path):
    """旧版 Word (.doc, 含 WPS 生成的二进制) → UTF-16LE 解码抽 CJK 片段。"""
    data = open(path, 'rb').read()
    text = data.decode('utf-16-le', errors='ignore')
    cjk = re.compile(r'[\u4e00-\u9fff0-9a-zA-Z，。；：、（）《》\"%\- ]{8,}')
    runs = cjk.findall(text)
    meta = re.compile(
        r'^(Root Entry|SummaryInformation|DocumentSummaryInformation|WordDocument|'
        r'KSOTemplateDocerSaveRecord|WpsCustomData|HYPERLINK|Administrator|F1E327BC|'
        r'KSOProductBuildVer|scnfvv|VjOSdC|搀洀椀渀|eyJo|1E2F9D6C)', re.I)
    out = []
    for r in runs:
        r = r.strip()
        if not r or meta.match(r):
            continue
        out.append(r)
    return '\n\n'.join(out)


def extract_docx(path):
    """Word 2007+ (.docx) → zipfile 读 document.xml 抽 <w:t>。"""
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
    paras = re.findall(r'<w:p[ >].*?</w:p>', xml, re.S)
    lines = []
    for para in paras:
        texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', para, re.S)
        line = ''.join(texts).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)


def extract_pdf(path):
    """PDF → 优先 pypdf，回退 pdfminer.six。"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        return '\n'.join((p.extract_text() or '') for p in reader.pages)
    except Exception:
        try:
            from pdfminer.high_level import extract_text
            return extract_text(path)
        except Exception as e:
            return f'[PDF 提取失败：{e}；请安装 pypdf 或 pdfminer.six]'


def extract_plain(path):
    return open(path, encoding='utf-8', errors='ignore').read()


def main():
    ap = argparse.ArgumentParser(description='会议录音文字版 → 校对底稿')
    ap.add_argument('--input', required=True, help='输入文件路径')
    ap.add_argument('--out', required=True, help='输出 txt 路径')
    args = ap.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext == '.doc':
        text = extract_doc(args.input)
    elif ext == '.docx':
        text = extract_docx(args.input)
    elif ext == '.pdf':
        text = extract_pdf(args.input)
    else:
        text = extract_plain(args.input)

    out_dir = os.path.dirname(args.out) or '.'
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'SAVED {args.out} | chars={len(text)}')


if __name__ == '__main__':
    main()
